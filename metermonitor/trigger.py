import collections
from . import Config, Zone
import logging

logger = logging.getLogger(__name__)


class Trigger:

    def __init__(self, number, zone1: Zone, zone2, config: Config):
        self.__zone1 = zone1
        self.__zone2 = zone2
        self.__config = config
        self.__number = number

        self.__lastState = [None, None]
        self.__state = [None, None]
        self.__sensible_state = True
        self.__fired = False

        self.__validStates = collections.deque(maxlen=4)
        self.__validStates.append([True, True])
        self.__validStates.append([False, True])
        self.__validStates.append([False, False])
        self.__validStates.append([True, False])

    def zones(self):
        return [self.__zone1, self.__zone2]

    def reset_expected_deque(self):
        while self.__validStates[0] != self.__state:
            self.__roll_forward()

    def update(self):
        self.__lastState = list(self.__state)
        self.__state = [self.__zone1.is_hot(), self.__zone2.is_hot()]

        if self.__has_changed() and self.__state != self.__expected_state():
            if self.sensible_state() is True:
                self.__roll_forward()
            self.__sensible_state = True
        elif self.__has_changed():
            self.__sensible_state = False

    @staticmethod
    def all_equal(a_list):
        return all(a_list[0] == item for item in a_list)

    def __expected_state(self):
        return self.__validStates[0]

    def __roll_forward(self):
        self.__validStates.rotate(-1)

    def __roll_back(self):
        self.__validStates.rotate(1)

    def fired(self):
        if self.__has_changed() and self.known_state() and self.sensible_state():
            if self.all_equal(self.__state):
                logger.debug("{} : {} -> {}".format(self.__number, self.__lastState, self.__state))
                return True

        return False

    def known_state(self):
        return None not in self.__lastState

    def sensible_state(self):
        return self.__sensible_state

    def __has_changed(self):
        return set(self.__lastState) != set(self.__state)

    def number(self):
        return self.__number