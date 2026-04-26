from rapidocr_onnxruntime import RapidOCR
from .base import BaseOCR

class RapidOCRWrapper(BaseOCR):
    def __init__(self):
        self.ocr = RapidOCR()

    def extract_text(self, image):
        result, _ = self.ocr(image)
        if result is None:
            return ""
        return " ".join([line[1] for line in result])