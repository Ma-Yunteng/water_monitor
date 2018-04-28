from . import Config, Camera, Meter
import logging

logger = logging.getLogger(__name__)


class Monitor:
    def __init__(self, config: Config, viewer, camera: Camera, meter: Meter):
        self.__online = True
        self.__viewer = viewer
        self.__camera = camera
        self.__config = config
        self.__meter = meter

    def poll(self):
        captured = self.__camera.capture()

        self.__online = captured is not None

        if self.__online:
            logger.debug("Frame captured")

            for zone in self.__meter.get_zones():
                rect = self.__camera.extract_rect(captured[-1], zone.x(), zone.y(), zone.w(), zone.h())
                is_hot = self.__camera.is_hot(rect)
                zone.update(is_hot)

            flow = self.__meter.recent_flow()

            logger.debug('Flow: %sL', flow)

            self.__viewer.render(captured, self.__meter)

            return 0
        else:
            if not self.__config.is_calibrate():
                logger.warning("Camera offline")
                self.__online = False

    def is_online(self):
        return self.__online
