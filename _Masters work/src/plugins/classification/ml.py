from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from src.utils.clean import clean_text


class MLClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression()

    def train(self, texts, labels):
        texts = [clean_text(t) for t in texts]
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)

    def classify(self, document):
        text = clean_text(document.raw_text)
        X = self.vectorizer.transform([text])
        return str(self.model.predict(X)[0])

