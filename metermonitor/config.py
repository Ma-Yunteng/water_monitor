import json
import os


class Config:

    def __init__(self, configuration, mode="LIVE"):
        if os.path.exists(configuration):
            self.__config = json.load(open(configuration))
        else:
            self.__config = json.loads(configuration)

        self.__mode = mode

    def videoSource(self):
        return self.__config["captureSource"]

    def mode(self):
        return self.__mode

    def isDebug(self):
        return "DEBUG" in self.mode()

    def isCalibrate(self):
        return "CALIBRATE" in self.mode()

    def meterFace(self):
        return self.__config["meterFace"]
