from unittest import TestCase
from metermonitor import Camera
import hashlib


class InitCameraTestConfig:

    @staticmethod
    def meter_face():
        meterface = dict()
        meterface["centrePoint"] = [20, 20]

        radius = dict()
        radius["inner"] = 5
        radius["outer"] = 10
        meterface["radius"] = radius

        return meterface


class TestCamera(TestCase):

    def test_init_getsCorrectValuesFromConfig(self):

        device = dict()
        device["source"] = "./tests/video/video0.avi"

        camera = Camera(device, InitCameraTestConfig().meter_face())
        self.assertEquals(camera.radii(), ([20, 20], 5, 10))

    def test_validVideoSource_cameraIsOnline(self):

        device = dict()
        device["source"] = "./tests/video/video0.avi"

        camera = Camera(device, InitCameraTestConfig().meter_face())

        self.assertTrue(camera.is_online())

    def test_validVideoSource_cameraIsOnline(self):

        device = dict()
        device["source"] = "/tmp/NON_EXISTENT_FILE"

        camera = Camera(device, InitCameraTestConfig().meter_face())

        self.assertFalse(camera.is_online())


class CameraIntegrationTestConfig:

    @staticmethod
    def meter_face():
        meterface = dict()
        meterface["centrePoint"] = [310, 300]

        radius = dict()
        radius["inner"] = 230
        radius["outer"] = 280
        meterface["radius"] = radius

        return meterface


class TestCameraIntegration(TestCase):

    def test_integration_cameraCapture(self):
        device = dict()
        device["source"] = "./tests/video/video0.avi"

        camera = Camera(device, CameraIntegrationTestConfig().meter_face())

        self.assertTrue(camera.is_online())

        for x in range(100):
            camera.capture()

        frame101 = camera.capture()

        raw = hashlib.md5(frame101[0].data).hexdigest()
        self.assertEquals(raw, 'bb1e80efb3e9f024499f04cd229773e1')
        self.assertEquals(frame101[0].shape, (480, 640, 3))

        grayscale = hashlib.md5(frame101[1].data).hexdigest()
        self.assertEquals(grayscale, '579b098751943db1932cf53719297671')
        self.assertEquals(frame101[1].shape, (480, 640))

        masked = hashlib.md5(frame101[2].data).hexdigest()
        self.assertEquals(masked, 'e86328cf25e5241fc12fc5c933af568a')
        self.assertEquals(frame101[2].shape, (480, 640))

        contrast_adjusted = hashlib.md5(frame101[3].data).hexdigest()
        self.assertEquals(contrast_adjusted, 'c2e863e9e5fd46d515d8af326b635f09')
        self.assertEquals(frame101[3].shape, (480, 640))

        camera.shutdown()


