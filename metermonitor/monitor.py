from . import Config


class Monitor:

    def __init__(self, config: Config, viewer):
        self.__online = True
        self.__viewer = viewer
        self.__camera = Camera

    def poll(self):
        newFrame = capture(self.__camera)
        self.__online = newFrame is not None

        if self.__online:
            filteredFrame = self.filterFrame(newFrame)
            flowQty = self.__meter.update(filteredFrame)

            self.__viewer.render(newFrame, filteredFrame, self.__meter)

            return flowQty
        else:
            if not calibrate:
                raise Exception("camera offline!")

    def isOnline(self):
        return self.__online

    def filterFrame(self, rawFrame):
        return threshold(rawFrame)
