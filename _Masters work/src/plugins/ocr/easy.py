import easyocr
from .base import BaseOCR

class EasyOCRWrapper(BaseOCR):
    def __init__(self):
        self.reader = easyocr.Reader(['en'])

    def extract_text(self, image):
        result = self.reader.readtext(image, detail=0)
        return " ".join(result)