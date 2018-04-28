import cv2


class Camera:

    def __init__(self, device, meter_face):
        self.__device = cv2.VideoCapture(device["source"])
        self.__centre_point = meter_face["centrePoint"]
        self.__centre_radius = meter_face["radius"]["inner"]
        self.__outer_radius = meter_face["radius"]["outer"]

    def is_online(self):
        return self.__device.isOpened()

    def capture(self):
        raw = self.__device.read()[1]

        if raw is None:
            return None

        gray = cv2.cvtColor(raw, cv2.COLOR_RGB2GRAY)

        masked = gray.copy()
        self.mask_centre(masked, self.__centre_point, self.__centre_radius)
        self.mask_outside(masked, self.__centre_point, self.__outer_radius)

        contrast_adjusted = self.threshold(masked)

        return raw, gray, masked, contrast_adjusted

    def shutdown(self):
        cv2.destroyAllWindows()
        self.__device.release()

    @staticmethod
    def is_hot(img):
        return cv2.mean(img)[0] < 128.0

    @staticmethod
    def extract_rect(img, x, y, w, h):
        if img is None:
            return None

        return img[y:y + h, x:x + w]

    @staticmethod
    def draw_circle(img, centre, radius, colour, thickness):
        cv2.circle(img, (centre[0], centre[1]), radius, (colour, colour, colour), thickness)

    def mask_centre(self, img, centre, radius):
        self.draw_circle(img, centre, radius, 0, -1)

    def mask_outside(self, img, centre, radius):
        thickness = 1000
        self.draw_circle(img, centre, int(radius + (thickness / 2)), 0, thickness)

    @staticmethod
    def threshold(img):
        retval, threshold = cv2.threshold(img, 150, 255, cv2.THRESH_OTSU)

        return threshold
