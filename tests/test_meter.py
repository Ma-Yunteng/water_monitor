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


def update_meter_zones(meter, update_data):
    i = 0

    for zone in meter.get_zones():
        zone.update(update_data[i])
        i = i + 1

    return meter.recent_flow()


class TestMeterWithRealisticTriggers(TestCase):

    def setUp(self):
        trigger_config = json.loads("""[[
        {
            "angle": -93,
            "offset": 0,
            "size": 25
        },
        {
            "angle": -86,
            "offset": 0,
            "size": 25
        }
    ],
    [
        {
            "angle": -74,
            "offset": 0,
            "size": 25
        },
        {
            "angle": -67,
            "offset": 0,
            "size": 25
        }
    ],
    [
        {
            "angle": -55,
            "offset": 0,
            "size": 25
        },
        {
            "angle": -48,
            "offset": 0,
            "size": 25
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

        self.meter = Meter(TestConfig(trigger_config, sample_meter_face))

    def test_correctCycle_triggersAtExpectedPoints(self):
        self.assertEqual(0, update_meter_zones(self.meter, [False, False, False, False, False, False]))
        self.assertEqual(0, update_meter_zones(self.meter, [False, False, False, False, False, False]))

        self.assertEqual(0, update_meter_zones(self.meter, [True, False, False, False, False, False]))
        self.assertEqual(1, update_meter_zones(self.meter, [True, True, False, False, False, False]))
        self.assertEqual(0, update_meter_zones(self.meter, [True, True, True, False, False, False]))
        self.assertEqual(1, update_meter_zones(self.meter, [True, True, True, True, False, False]))
        self.assertEqual(0, update_meter_zones(self.meter, [True, True, True, True, True, False]))
        self.assertEqual(1, update_meter_zones(self.meter, [True, True, True, True, True, True]))
        self.assertEqual(0, update_meter_zones(self.meter, [False, True, True, True, True, True]))
        self.assertEqual(1, update_meter_zones(self.meter, [False, False, True, True, True, True]))
