from sklearn.metrics import classification_report, accuracy_score

from src.plugins.tf_idf_vectorizer import TfidfVectorizerCustom
from src.plugins.text_preprocessor import TextPreprocessor
from src.plugins.dataset_preprocessor import DatasetPreprocessor

from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import math
import random


def plot_top_words(model, vectorizer, class_id=2, top_n=20):
    """
    Визуализация самых важных слов для выбранного класса
    """

    # 1. индекс → слово
    index_to_word = {i: w for w, i in vectorizer.vocab.items()}

    # 2. берём модель конкретного класса (OVR)
    clf = model.models[class_id]

    # 3. собираем (слово, вес)
    word_weights = []

    for idx, weight in enumerate(clf.w):
        if idx in index_to_word:
            word = index_to_word[idx]
            word_weights.append((word, weight))

    # 4. сортируем
    top_positive = sorted(word_weights, key=lambda x: x[1], reverse=True)[:top_n]
    top_negative = sorted(word_weights, key=lambda x: x[1])[:top_n]

    # 5. распаковка
    pos_words, pos_vals = zip(*top_positive)
    neg_words, neg_vals = zip(*top_negative)

    # 6. рисуем график
    plt.figure(figsize=(12, 6))

    # positive
    plt.barh(pos_words[::-1], pos_vals[::-1], color="green", label="positive influence")

    # negative
    plt.barh(neg_words[::-1], neg_vals[::-1], color="red", label="negative influence")

    plt.title(f"Top words for class {class_id}")
    plt.xlabel("Weight")
    plt.legend()

    plt.tight_layout()
    plt.show()


def compute_class_weights(labels):
    counts = Counter(labels)
    total = sum(counts.values())
    num_classes = len(counts)

    return {
        cls: total / (num_classes * count)
        for cls, count in counts.items()
    }


class LogisticRegressionBinary:
    def __init__(self, n_features, lr=0.1, epochs=10):
        self.n_features = n_features
        self.lr = lr
        self.epochs = epochs

        self.w = [0.0] * n_features
        self.b = 0.0

    def fit(self, X, y, sample_weights=None):
        for epoch in range(self.epochs):
            for i, (xi, yi) in enumerate(zip(X, y)):
                z = self.dot_product(self.w, xi) + self.b
                p = self.sigmoid(z)

                error = p - yi

                weight = sample_weights[i] if sample_weights else 1.0

                # обновляем веса
                for j, v in xi.items():
                    self.w[j] -= self.lr * error * v * weight

                # обновляем сдвиг
                self.b -= self.lr * error * weight

    def predict_proba(self, X):
        probs = []
        for xi in X:
            z = self.dot_product(self.w, xi) + self.b
            probs.append(self.sigmoid(z))
        return probs

    def predict(self, X, threshold=0.5):
        probs = self.predict_proba(X)
        return [1 if p >= threshold else 0 for p in probs]

    @staticmethod
    def sigmoid(z):
        return 1 / (1 + math.exp(-z))

    @staticmethod
    def dot_product(w, x):
        # x — dict
        return sum(w[i] * v for i, v in x.items())


class LogisticRegressionOVR:
    def __init__(self, n_features, lr=0.1, epochs=10):
        self.n_features = n_features
        self.lr = lr
        self.epochs = epochs
        self.models = {}
        self.classes = []

    def fit(self, X, y, class_weights=None):
        self.classes = sorted(set(y))

        if class_weights is None:
            class_weights = {}


        for cls in self.classes:
            print(f"Training class {cls} vs rest")

            y_binary = [1 if label == cls else 0 for label in y]

            # веса для каждого объекта
            sample_weights = []
            for label in y:
                if label == cls:
                    sample_weights.append(class_weights.get(cls, 1))
                else:
                    sample_weights.append(1)

            model = LogisticRegressionBinary(
                n_features=self.n_features,
                lr=self.lr,
                epochs=self.epochs
            )

            model.fit(X, y_binary, sample_weights)
            self.models[cls] = model

    def predict(self, X):
        predictions = []

        for xi in X:
            class_scores = {}

            for cls, model in self.models.items():
                z = self.dot_product(model.w, xi) + model.b
                prob = self.sigmoid(z)
                class_scores[cls] = prob

            # выбираем класс с максимальной вероятностью
            predicted_class = max(class_scores, key=class_scores.get)
            predictions.append(predicted_class)

        return predictions

    @staticmethod
    def sigmoid(z):
        return 1 / (1 + math.exp(-z))

    @staticmethod
    def dot_product(w, x):
        # x — dict
        return sum(w[i] * v for i, v in x.items())


class TextClassifier:
    def __init__(self, max_features=50000, n_components=500, class_weights=None, random_state=42):
        self.max_features = max_features
        self.n_components = n_components
        self.class_weights = class_weights
        self.random_state = random_state

        self.vectorizer = TfidfVectorizerCustom(max_features=self.max_features)
        self.clf = None

    def prepare_data(self, corpus, labels, sample_size=50000, test_size=0.2):
        """Преобразует текст в векторы TF-IDF"""
        X = self.vectorizer.fit_transform(corpus[:sample_size])
        Y = labels[:sample_size]
        print(Counter(Y))

        # Пробовал уровнять кол-во объектов в обозреваемых классах = получилась жижа
        # X, Y = self.undersample(X, Y)
        # print(Counter(Y))

        self.X_train, self.X_test, self.y_train, self.y_test = self.train_test_split_custom(
            X=X, y=Y, test_size=test_size, random_state=self.random_state
        )

        self.clf = LogisticRegressionOVR(
            n_features=len(self.vectorizer.vocab),
            lr=0.05,
            epochs=30
        )

    def train(self):
        """Обучение логистической регрессии"""
        self.clf.fit(self.X_train, self.y_train, class_weights=self.class_weights)

    def evaluate(self):
        """Оценка точности и отчёт метрик"""
        y_pred = self.clf.predict(self.X_test)

        print("Accuracy:", accuracy_score(self.y_test, y_pred))
        print(classification_report(self.y_test, y_pred))

        plot_top_words(
            model=classifier.clf,
            vectorizer=classifier.vectorizer,
            class_id=2,
            top_n=15
        )

    @staticmethod
    def undersample(X, y):
        grouped = defaultdict(list)

        # группируем
        for xi, yi in zip(X, y):
            grouped[yi].append(xi)

        min_size = min(len(v) for v in grouped.values())

        new_X = []
        new_y = []

        for cls, items in grouped.items():
            sampled = random.sample(items, min_size)
            new_X.extend(sampled)
            new_y.extend([cls] * min_size)

        return new_X, new_y

    @staticmethod
    def train_test_split_custom(X, y, test_size=0.2, random_state=42):
        data = list(zip(X, y))
        random.seed(random_state)
        random.shuffle(data)

        split_idx = int(len(data) * (1 - test_size))
        train_data = data[:split_idx]
        test_data = data[split_idx:]

        X_train, y_train = zip(*train_data)
        X_test, y_test = zip(*test_data)

        return list(X_train), list(X_test), list(y_train), list(y_test)

    @staticmethod
    def from_dataset(sample_size=5000):
        """Удобный метод для создания и подготовки модели из датасета"""
        ds = TextPreprocessor.get_dataset()
        labels = DatasetPreprocessor.get_labels(dataset=ds, size=sample_size)
        tokenized_texts = DatasetPreprocessor.get_tokens(dataset=ds)
        weights = compute_class_weights(labels)
        print(weights)

        model = TextClassifier(max_features=sample_size, class_weights=weights)
        model.prepare_data(tokenized_texts, labels, sample_size=sample_size)
        return model


if __name__ == "__main__":

    classifier = TextClassifier.from_dataset()
    classifier.train()
    classifier.evaluate()