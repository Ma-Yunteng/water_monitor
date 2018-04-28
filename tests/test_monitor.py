from unittest import TestCase
from metermonitor import Monitor


class TestMonitor(TestCase):

    def setUp(self):
        self.monitor = Monitor(None, None, None, None)

    def test_justSetup_knownState_isFalse(self):
        self.assertTrue(self.monitor.is_online())
