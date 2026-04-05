import numpy as np
from collections import Counter

class TFIDFVectorizer:
    def __init__(self, max_vocab_size=5000):
        self.max_vocab_size = max_vocab_size
        self.word2idx = {}
        self.idf = None
        self.vocab_size = 0

    def fit(self, corpus):
        """
        Построение словаря и IDF на корпусе
        corpus: список списков токенов
        """
        # 1. Считаем все слова
        word_counts = Counter()
        for tokens in corpus:
            word_counts.update(tokens)

        # 2. Ограничиваем словарь
        most_common_words = word_counts.most_common(self.max_vocab_size)
        self.word2idx = {word: idx for idx, (word, _) in enumerate(most_common_words)}
        self.vocab_size = len(self.word2idx)

        # 3. DF и IDF
        N = len(corpus)
        df = np.zeros(self.vocab_size)
        for tokens in corpus:
            unique_tokens = set(tokens)
            for token in unique_tokens:
                if token in self.word2idx:
                    df[self.word2idx[token]] += 1
        self.idf = np.log(N / (1 + df))  # +1 чтобы не делить на 0

    def transform(self, corpus):
        """
        Преобразование документов в TF-IDF вектора
        """
        X = np.zeros((len(corpus), self.vocab_size))
        for i, tokens in enumerate(corpus):
            tf = np.zeros(self.vocab_size)
            for token in tokens:
                if token in self.word2idx:
                    tf[self.word2idx[token]] += 1
            if len(tokens) > 0:
                tf = tf / len(tokens)  # нормировка TF
            X[i] = tf * self.idf  # TF-IDF
        return X

    def fit_transform(self, corpus):
        """
        Удобный метод: сначала fit, потом transform
        """
        self.fit(corpus)
        return self.transform(corpus)