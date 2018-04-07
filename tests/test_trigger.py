from unittest import TestCase
from metermonitor import Trigger, Zone, Config


class TestConfig:
    def isDebug(self):
        return False

    def isCalibrate(self):
        return False


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

        self.trigger.update(update_data)

        self.assertFalse(self.trigger.known_state())
        self.assertFalse(self.trigger.fired())

    def test_update_sameAsLastState_stateIsKnown(self):
        update_data = [True, True]

        self.trigger.update(update_data)
        self.trigger.update(update_data)

        self.assertTrue(self.trigger.known_state())

    def test_update_sameAsLastState_notFired(self):
        update_data = [True, True]

        self.trigger.update(update_data)
        self.trigger.update(update_data)

        self.assertFalse(self.trigger.fired())

    def test_update_validateRealCycle(self):
        self.trigger.update([True, True])
        self.trigger.update([True, True])

        self.trigger.update([False, True])
        self.assertFalse(self.trigger.fired())

        self.trigger.update([False, False])
        self.assertTrue(self.trigger.fired())

        self.trigger.update([True, False])
        self.assertFalse(self.trigger.fired())

        self.trigger.update([True, True])
        self.assertTrue(self.trigger.fired())

    def test_update_sensorBounce_doesNotFire(self):
        self.trigger.update([True, True])
        self.trigger.update([True, True])

        self.trigger.update([False, True])
        self.assertFalse(self.trigger.fired())

        # sensor bounces
        self.trigger.update([True, True])
        self.assertFalse(self.trigger.fired())
        self.assertFalse(self.trigger.sensible_state())

        # sensor rebounds
        self.trigger.update([False, True])
        self.assertTrue(self.trigger.sensible_state())
        self.assertFalse(self.trigger.fired())

    def test_update_sensorBounceSeveralFrames_doesNotFire(self):
        self.trigger.update([True, True])
        self.trigger.update([True, True])

        self.trigger.update([False, True])
        self.assertFalse(self.trigger.fired())

        # sensor bounces and stays "wrong" for several frames
        self.trigger.update([True, True])
        self.assertFalse(self.trigger.fired())
        self.assertFalse(self.trigger.sensible_state())
        self.trigger.update([True, True])
        self.assertFalse(self.trigger.fired())
        self.assertFalse(self.trigger.sensible_state())
        self.trigger.update([True, True])
        self.assertFalse(self.trigger.fired())
        self.assertFalse(self.trigger.sensible_state())

        # sensor rebounds eventually
        self.trigger.update([False, True])
        self.assertTrue(self.trigger.sensible_state())
        self.assertFalse(self.trigger.fired())

    def test_update_sensorBounce_recoversAndFires(self):
        self.trigger.update([True, True])
        self.trigger.update([True, True])
        self.trigger.update([False, True])

        # sensor bounces
        self.trigger.update([True, True])

        # sensor rebounds
        self.trigger.update([False, True])

        # should now fire
        self.trigger.update([False, False])
        self.assertTrue(self.trigger.fired())

