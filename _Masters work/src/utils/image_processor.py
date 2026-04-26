import cv2

class Preprocessor:
    def __init__(self):
        pass

    def to_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    def to_blur(self, image):
        return cv2.GaussianBlur(image, (3, 3), 0)

    def threshold(self, image):
        th = cv2.adaptiveThreshold(
            image,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )
        return th

    def process(self, image):
        gray = self.to_grayscale(image)
        blur_gray = self.to_blur(gray)
        thresh = self.threshold(blur_gray)

        return thresh