import cv2


class Viewer:

    def show(self, frame):
        cv2.waitKey(10)
        cv2.imshow('frame', frame)

    def render(self, raw_frame, filtered_frame, meter):
        cv2.waitKey(10)

        raw_copy = raw_frame.copy()
        filter_copy = filtered_frame.copy()

        # for zone in meter.getZones():
        #
        #     zoneImg = extractRect(filter_copy, zone.x(), zone.y(), zone.w(), zone.h())
        #
        #     drawRect(raw_copy, zone.x(), zone.y(), zone.w(), zone.h(), 0)
        #     if zone.is_hot():
        #         drawRect(filter_copy, zone.x(), zone.y(), zone.w(), zone.h(), 255)
        #     else:
        #         drawRect(filter_copy, zone.x(), zone.y(), zone.w(), zone.h(), 0)

        cv2.imshow('raw', raw_copy)
        cv2.imshow('filtered', filter_copy)
