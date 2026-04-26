
from .base import BaseOCR
import pytesseract

class TesseractOCR(BaseOCR):
    def extract_text(self, image):
        return pytesseract.image_to_string(image)