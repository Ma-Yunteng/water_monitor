import json
import os


class Config:

    def __init__(self, configuration, mode="LIVE"):
        if os.path.exists(configuration):
            with open(configuration, 'r') as conf_file:
                self.__config = json.load(conf_file)
        else:
            self.__config = json.loads(configuration)

        self.__mode = mode

    def name(self):
        return self.__config["name"]

    def sensitivity(self):
        return self.__config["sensitivity"]

    def triggers(self):
        return self.__config["triggers"]

    def device(self):
        return self.__config["device"]

    def mode(self):
        return self.__mode

    def is_debug(self):
        return "DEBUG" in self.mode()

    def is_calibrate(self):
        return "CALIBRATE" in self.mode()

    def meter_face(self):
        return self.__config["meterFace"]
