import collections
from . import Config, Trigger, Zone
import math
import logging

logger = logging.getLogger(__name__)


class Meter:

    def __init__(self, config: Config):
        self.__config = config
        self.__name = config.name()
        self.__lastFired = None
        self.__sensitivity = config.sensitivity()
        self.__triggers, self.__fireDeque, self.__zones = self.__setup_triggers(config)

    @staticmethod
    def __rotate(point, radians, origin):
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

    @staticmethod
    def __array_to_zone(array):
        x = array[0]
        y = array[1]
        size = array[2]

        left = int(x - (size / 2))
        top = int(y - (size / 2))

        return Zone(left, top, array[2])

    def __get_zone_by_angle(self, meter_face, degrees, radius_offset, size):
        origin = meter_face["centrePoint"]
        trigger_radius = meter_face["radius"]["trigger"]
        zero_angle_offset = meter_face["zeroAngle"]

        zero_angle_point = (origin[0] - trigger_radius - radius_offset, origin[1])
        zero_angle_point = self.__rotate(zero_angle_point, self.__degrees_to_clockwise_rads(zero_angle_offset), origin)
        rotated_point = self.__rotate(zero_angle_point, self.__degrees_to_clockwise_rads(degrees), origin)
        rotated_angle_zone = self.__array_to_zone([rotated_point[0], rotated_point[1], size])

        return rotated_angle_zone

    def __get_zone_from_config(self, meter_face, item):
        return self.__get_zone_by_angle(meter_face, item["angle"], item["offset"], item["size"])

    def __setup_triggers(self, config: Config):
        fire_deque = collections.deque(maxlen=len(config.triggers()))
        triggers = []
        zones = []

        trig_count = 0

        for trig_config in config.triggers():
            zone0 = self.__get_zone_from_config(config.meter_face(), trig_config[0])
            zone1 = self.__get_zone_from_config(config.meter_face(), trig_config[1])
            new_trigger = Trigger(trig_count, zone0, zone1, config)

            triggers.append(new_trigger)
            fire_deque.append(new_trigger)
            zones.extend(new_trigger.zones())

            trig_count = trig_count + 1

        return triggers, fire_deque, zones

    def handle_calibration_error(self, message):
        if self.__config.is_calibrate():
            logger.warning(message)
        else:
            raise Exception(message)

    def recent_flow(self):
        fired = []
        for trigger in self.__triggers:
            trigger.update()
            if trigger.fired():
                fired.append(trigger)

        if len(fired) > 1:
            self.handle_calibration_error("Two triggers ({}) fired together?".format(fired))

        if len(fired) == 1:
            if self.__lastFired is None:
                while self.__fireDeque[0] is not fired[0]:
                    self.__fireDeque.rotate(-1)
                self.__fireDeque.rotate(1)

            self.__lastFired = fired[0]
            self.__fireDeque.rotate(-1)

            if self.__fireDeque[0] is not self.__lastFired:
                self.handle_calibration_error("Unexpected trigger {} fired!".format(fired))
            else:
                return self.__sensitivity

        return 0

    def get_zones(self):
        return self.__zones
