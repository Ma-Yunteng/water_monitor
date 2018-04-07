from unittest import TestCase
from metermonitor import Trigger, Zone


class TestConfig:
    def is_debug(self):
        return False

    def is_calibrate(self):
        return False


def update_trigger_zones(trigger: Trigger, update_data):
    trigger.zones()[0].update(update_data[0])
    trigger.zones()[1].update(update_data[1])
    trigger.update()


class TestTrigger(TestCase):

    def setUp(self):
        self.zone1 = Zone(1, 2, 3)
        self.zone2 = Zone(4, 5, 6)

        self.trigger = Trigger(1, self.zone1, self.zone2, TestConfig())

    def test_justSetup_knownState_isFalse(self):
        self.assertFalse(self.trigger.known_state())

    def test_justSetup_sensibleState_isTrue(self):
        self.assertTrue(self.trigger.sensible_state())

    def test_fired_nothingChanged_returnsFalse(self):
        self.assertFalse(self.trigger.fired())

    def test_update_afterFirstUpdate_stillUnknownState(self):
        update_data = [True, True]

        update_trigger_zones(self.trigger, update_data)

        self.assertFalse(self.trigger.known_state())
        self.assertFalse(self.trigger.fired())

    def test_update_sameAsLastState_stateIsKnown(self):
        update_data = [True, True]

        update_trigger_zones(self.trigger, update_data)
        update_trigger_zones(self.trigger, update_data)

        self.assertTrue(self.trigger.known_state())

    def test_update_sameAsLastState_notFired(self):
        update_data = [True, True]

        update_trigger_zones(self.trigger, update_data)
        update_trigger_zones(self.trigger, update_data)

        self.assertFalse(self.trigger.fired())

    def test_update_validateRealCycle(self):
        update_trigger_zones(self.trigger, [True, True])
        update_trigger_zones(self.trigger, [True, True])

        update_trigger_zones(self.trigger, [False, True])
        self.assertFalse(self.trigger.fired())

        update_trigger_zones(self.trigger, [False, False])
        self.assertTrue(self.trigger.fired())

        update_trigger_zones(self.trigger, [True, False])
        self.assertFalse(self.trigger.fired())

        update_trigger_zones(self.trigger, [True, True])
        self.assertTrue(self.trigger.fired())

    def test_update_sensorBounce_doesNotFire(self):
        update_trigger_zones(self.trigger, [True, True])
        update_trigger_zones(self.trigger, [True, True])

        update_trigger_zones(self.trigger, [False, True])
        self.assertFalse(self.trigger.fired())

        # sensor bounces
        update_trigger_zones(self.trigger, [True, True])
        self.assertFalse(self.trigger.fired())
        self.assertFalse(self.trigger.sensible_state())

        # sensor rebounds
        update_trigger_zones(self.trigger, [False, True])
        self.assertTrue(self.trigger.sensible_state())
        self.assertFalse(self.trigger.fired())

    def test_update_sensorBounceSeveralFrames_doesNotFire(self):
        update_trigger_zones(self.trigger, [True, True])
        update_trigger_zones(self.trigger, [True, True])

        update_trigger_zones(self.trigger, [False, True])
        self.assertFalse(self.trigger.fired())

        # sensor bounces and stays "wrong" for several frames
        update_trigger_zones(self.trigger, [True, True])
        self.assertFalse(self.trigger.fired())
        self.assertFalse(self.trigger.sensible_state())
        update_trigger_zones(self.trigger, [True, True])
        self.assertFalse(self.trigger.fired())
        self.assertFalse(self.trigger.sensible_state())
        update_trigger_zones(self.trigger, [True, True])
        self.assertFalse(self.trigger.fired())
        self.assertFalse(self.trigger.sensible_state())

        # sensor rebounds eventually
        update_trigger_zones(self.trigger, [False, True])
        self.assertTrue(self.trigger.sensible_state())
        self.assertFalse(self.trigger.fired())

    def test_update_sensorBounce_recoversAndFires(self):
        update_trigger_zones(self.trigger, [True, True])
        update_trigger_zones(self.trigger, [True, True])
        update_trigger_zones(self.trigger, [False, True])

        # sensor bounces
        update_trigger_zones(self.trigger, [True, True])

        # sensor rebounds
        update_trigger_zones(self.trigger, [False, True])

        # should now fire
        update_trigger_zones(self.trigger, [False, False])
        self.assertTrue(self.trigger.fired())
