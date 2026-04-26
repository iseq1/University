class Pipeline:
    def __init__(self, ocr, structurer, classifier):
        self.ocr = ocr
        self.structurer = structurer
        self.classifier = classifier

    def run(self, image):
        text = self.ocr.extract_text(image)
        document = self.structurer.structure(text)
        category = self.classifier.classify(document)

        return {
            "text": text,
            "structured": document.fields,
            "category": category
        }