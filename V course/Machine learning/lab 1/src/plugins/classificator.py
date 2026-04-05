import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

from text_preprocessor import TextPreprocessor
from dataset_preprocessor import DatasetPreprocessor

class TextClassifier:
    def __init__(self, max_features=50000, n_components=500, class_weights=None, random_state=42):
        self.max_features = max_features
        self.n_components = n_components
        self.class_weights = class_weights
        self.random_state = random_state

        self.vectorizer = TfidfVectorizer(max_features=self.max_features)
        self.svd = TruncatedSVD(n_components=self.n_components)
        self.clf = LogisticRegression(
            solver='saga',
            max_iter=2000,
            class_weight=self.class_weights
        )

    def prepare_data(self, corpus, labels, sample_size=50000, test_size=0.2):
        """Преобразует текст в векторы TF-IDF и уменьшает размерность"""
        texts_str = [" ".join(tokens) for tokens in corpus[:sample_size]]
        X = self.vectorizer.fit_transform(texts_str)
        X_reduced = self.svd.fit_transform(X)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X_reduced, labels[:sample_size],
            test_size=test_size,
            random_state=self.random_state,
            stratify=labels[:sample_size]
        )

    def train(self):
        """Обучение логистической регрессии"""
        self.clf.fit(self.X_train, self.y_train)

    def evaluate(self):
        """Оценка точности и отчёт метрик"""
        y_pred = self.clf.predict(self.X_test)
        print("Accuracy:", accuracy_score(self.y_test, y_pred))
        print(classification_report(self.y_test, y_pred))

    @staticmethod
    def from_dataset(sample_size=50000, class_weights=None):
        """Удобный метод для создания и подготовки модели из датасета"""
        ds = TextPreprocessor.get_dataset()
        labels = DatasetPreprocessor.get_labels(dataset=ds)
        tokenized_texts = DatasetPreprocessor.get_tokens(dataset=ds)

        model = TextClassifier(class_weights=class_weights)
        model.prepare_data(tokenized_texts, labels, sample_size=sample_size)
        return model

# =========================
# ПРИМЕР ИСПОЛЬЗОВАНИЯ
# =========================
if __name__ == "__main__":
    weights = {0: 1, 1: 4, 2: 1, 3: 4}

    classifier = TextClassifier.from_dataset(class_weights=weights)
    classifier.train()
    classifier.evaluate()