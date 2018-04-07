from . import Config
from . import Camera


class Monitor:

    def __init__(self, config: Config, viewer, camera: Camera):
        self.__online = True
        self.__viewer = viewer
        self.__camera = camera
        self.__config = config

    def poll(self):
        new_frame = self.__camera.capture()
        self.__online = new_frame is not None

        # if self.__online:
        #     filtered_frame = self.filter_frame(new_frame)
        #     flow_qty = self.__meter.update(filtered_frame)
        #
        #     self.__viewer.render(new_frame, filtered_frame, self.__meter)
        #
        #     return flow_qty
        # else:
        #     if not self.__config.is_calibrate():
        #         raise Exception("camera offline!")

    def is_online(self):
        return self.__online

    # @staticmethod
    # def filter_frame(raw_frame):
    #     return threshold(raw_frame)
