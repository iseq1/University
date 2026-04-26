from src.utils.doc_structe import Document
from .base import BaseStructurer

class SimpleStructurer(BaseStructurer):
    def structure(self, text):
        return Document(
            raw_text=text,
            fields={
                "length": len(text),
                "has_total": "total" in text.lower()
            }
        )