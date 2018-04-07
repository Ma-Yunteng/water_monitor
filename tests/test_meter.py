from unittest import TestCase
from metermonitor import Meter


class TestConfig:

    def __init__(self, triggers=[]):
        self.__triggers = triggers

    @staticmethod
    def is_debug():
        return False

    @staticmethod
    def is_calibrate():
        return False

    @staticmethod
    def name():
        return "Test"

    @staticmethod
    def sensitivity():
        return 1

    def triggers(self):
        return self.__triggers


class TestMeter(TestCase):

    def setUp(self):
        self.meter = Meter(TestConfig())

    def test_emptyMeter_recentFlowIsZero(self):
        self.assertEquals(self.meter.recent_flow(), 0)

    def test_emptyMeter_noZones(self):
        self.assertEquals(len(self.meter.get_zones()), 0)
