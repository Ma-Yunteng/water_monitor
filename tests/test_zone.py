import unittest
from metermonitor import Zone


class TestZone(unittest.TestCase):
    def test_is_hot_newZone_isNotHot(self):
        new_zone = Zone(1, 2, 3)

        self.assertFalse(new_zone.is_hot())


if __name__ == '__main__':
    unittest.main()
