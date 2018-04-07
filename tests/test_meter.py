from unittest import TestCase
from metermonitor import Meter
import json


class TestConfig:

    def __init__(self, trigger_config=[], meter_face=None):
        self.__triggers = trigger_config
        self.__meter_face = meter_face

    @staticmethod
    def is_debug():
        return False

    @staticmethod
    def is_calibrate():
        return False

    @staticmethod
    def name():
        return "Test"

    def meter_face(self):
        return self.__meter_face

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

    def test_initWithTriggers_triggersAtCorrectPoints(self):
        trigger_config = json.loads("""[[
{
    "angle": 0,
    "offset": 0,
    "size": 10
},
{
    "angle": -45,
    "offset": 0,
    "size": 10
}
]]""")

        sample_meter_face = json.loads("""{
    "centrePoint": [1000, 1000],
    "radius": {
        "inner": 100,
        "outer": 300,
        "trigger": 200
    },
    "zeroAngle": 90
}""")

        meter = Meter(TestConfig(trigger_config, sample_meter_face))

        expected_0 = (995, 795, 10, 10)
        expected_1 = (853, 853, 10, 10)

        self.assertEqual(meter.get_zones()[0].raw(), expected_0)
        self.assertEqual(meter.get_zones()[1].raw(), expected_1)

        self.assertEqual(len(meter.get_zones()), 2)
