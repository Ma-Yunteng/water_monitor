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

            self.__viewer.render(captured[0], captured[2], self.__meter)

            return 0
        else:
            if not self.__config.is_calibrate():
                logger.warning("Camera offline")
                self.__online = False

    def is_online(self):
        return self.__online

    # @staticmethod
    # def filter_frame(raw_frame):
    #     return threshold(raw_frame)
