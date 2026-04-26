from .base import BaseClassifier
from src.utils.doc_structe import Document
from ...utils.clean import clean_text


class RuleClassifier(BaseClassifier):

    CATEGORIES = {
        "food": [
            "restaurant", "restaur", "mcdon", "burger", "pizza",
            "kfc", "coffee", "cafe", "meal", "fries"
        ],
        "transport": [
            "taxi", "uber", "lyft", "bus", "train",
            "ticket", "metro", "fuel", "gas"
        ],
        "shopping": [
            "amazon", "order", "purchase", "store",
            "item", "mall", "nike", "ikea"
        ],
        "utilities": [
            "bill", "electricity", "water", "internet",
            "rent", "insurance", "subscription"
        ]
    }

    def score_text(self, text):
        scores = {cat: 0 for cat in self.CATEGORIES}

        for category, keywords in self.CATEGORIES.items():
            for word in keywords:
                if word in text:
                    scores[category] += 1

        return scores

    def classify(self, document):
        text = document.raw_text.lower()

        scores = self.score_text(text)

        best_category = max(scores, key=scores.get)

        # если вообще ничего не нашли
        if scores[best_category] == 0:
            return "other"

        return best_category
