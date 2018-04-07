import cv2


class Viewer:

    def show(self, frame):
        cv2.waitKey(10)
        cv2.imshow('frame', frame)

    def render(self, rawFrame, filteredFrame, meter):
        cv2.waitKey(10)

        rawCopy = rawFrame.copy()
        filterCopy = filteredFrame.copy()

        for zone in meter.getZones():

            zoneImg = extractRect(filterCopy, zone.x(), zone.y(), zone.w(), zone.h())

            drawRect(rawCopy, zone.x(), zone.y(), zone.w(), zone.h(), 0)
            if zone.is_hot():
                drawRect(filterCopy, zone.x(), zone.y(), zone.w(), zone.h(), 255)
            else:
                drawRect(filterCopy, zone.x(), zone.y(), zone.w(), zone.h(), 0)

        cv2.imshow('raw', rawCopy)
        cv2.imshow('filtered', filterCopy)


