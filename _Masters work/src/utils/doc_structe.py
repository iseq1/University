class Document:
    def __init__(self, raw_text, fields=None):
        self.raw_text = raw_text
        self.fields = fields or {}