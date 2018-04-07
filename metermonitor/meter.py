import collections
from . import Config, Trigger
import math


class Meter:

    def __init__(self, config: Config):
        self.__config = config
        self.__name = config.name()
        self.__lastFired = None
        self.__sensitivity = config.sensitivity()
        self.__triggers = []
        self.__zones = []
        self.__setup_triggers(config.triggers())
        self.__fireDeque = collections.deque(maxlen=len(self.__triggers))

        trigCount = 0

        for item in self.__triggers:
            self.__fireDeque.append(item)
            self.__zones.extend(item.zones())
            item.set_number(trigCount)
            trigCount = trigCount + 1

    @staticmethod
    def __rotate_around_point_lowperf(point, radians, origin=(0, 0)):
        """
        From https://ls3.io/post/rotate_a_2d_coordinate_around_a_point_in_python/
        """
        x, y = point
        ox, oy = origin

        qx = ox + math.cos(radians) * (x - ox) + math.sin(radians) * (y - oy)
        qy = oy + -math.sin(radians) * (x - ox) + math.cos(radians) * (y - oy)

        return qx, qy

    @staticmethod
    def __degrees_to_clockwise_rads(degrees):
        return math.radians(degrees) * -1

    def __get_zone_by_angle(self, degrees, radius_offset, size):
        origin = self.__config.meter_face()["centrePoint"]
        trigger_radius = self.__config.meter_face()["radius"]["trigger"]
        zero_angle_offset = self.__config.meter_face()["zeroAngle"]

        zero_angle_point = (origin[0] - trigger_radius - radius_offset, origin[1])
        zero_angle_point = self.__rotate_around_point_lowperf(zero_angle_point, self.__degrees_to_clockwise_rads(zero_angle_offset), origin)
        rotated_point = self.__rotate_around_point_lowperf(zero_angle_point, self.__degrees_to_clockwise_rads(degrees), origin)
        rotated_angle_zone = self.__arrayToZone([rotated_point[0], rotated_point[1], size])

        return rotated_angle_zone

    def __get_zone_from_config(self, item):
        return self.__get_zone_by_angle(item["angle"], item["offset"], item["size"])

    def __setup_triggers(self, trigger_config):
        for trigger in trigger_config:
            zone0 = self.__get_zone_from_config(trigger[0])
            zone1 = self.__get_zone_from_config(trigger[1])
            self.__triggers.append(Trigger(zone0, zone1))

    def update(self, data):
        fired = []
        for trigger in self.__triggers:
            trigger.update(data)
            if trigger.fired():
                fired.append(trigger)

        if len(fired) > 1 and not self.__config.is_calibrate():
            raise Exception("Two triggers fired together?")

        if len(fired) == 1:
            if self.__lastFired is None:
                while self.__fireDeque[0] is not fired[0]:
                    self.__fireDeque.rotate(-1)
                self.__fireDeque.rotate(1)

            self.__lastFired = fired[0]
            self.__fireDeque.rotate(-1)

            if self.__fireDeque[0] is not self.__lastFired and not self.__config.is_calibrate():
                raise Exception("Unexpected trigger fired!")
            else:
                return self.__sensitivity

        return 0

    def getZones(self):
        return self.__zones
