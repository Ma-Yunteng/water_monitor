import cv2


class Camera:

    def __init__(self, device):
        self.__device = cv2.VideoCapture(device["source"])

    def isOnline(self):
        return self.__device.isOpened()

    def capture(self):
        raw = self.__device.read()[1]

        if raw is None:
            return None

        # removeBackground(raw)
        # maskCentre(raw, centrePoint, centreRadius)
        # maskOutside(raw, centrePoint, outsideRadius)

        gray = cv2.cvtColor(raw, cv2.COLOR_RGB2GRAY)

        return gray
