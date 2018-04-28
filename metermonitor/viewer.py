import cv2
from . import Meter


class Viewer:

    @staticmethod
    def draw_rect(img, x, y, w, h, colour):
        cv2.rectangle(img, (x, y), (x + w, y + h), (colour, colour, colour), 1)

    def render(self, frame_versions, meter: Meter):
        cv2.waitKey(10)

        window = 0

        for version in frame_versions:
            copied_frame = version.copy()

            for zone in meter.get_zones():

                if zone.is_hot():
                    black = 0
                    self.draw_rect(copied_frame, zone.x(), zone.y(), zone.w(), zone.h(), black)
                else:
                    white = 255
                    self.draw_rect(copied_frame, zone.x(), zone.y(), zone.w(), zone.h(), white)

            cv2.imshow(str(window), copied_frame)

            window = window + 1
