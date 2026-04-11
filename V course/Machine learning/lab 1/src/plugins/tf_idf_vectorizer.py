import math
from collections import Counter, defaultdict

class TfidfVectorizerCustom:
    def __init__(self, max_features=50000):
        self.max_features = max_features
        self.vocab = {}
        self.idf = {}

    def fit(self, corpus):
        """
        corpus: список документов, где каждый документ — список токенов
        """
        doc_freq = defaultdict(int)
        total_docs = len(corpus)

        # считаем document frequency
        for doc in corpus:
            unique_words = set(doc)
            for word in unique_words:
                doc_freq[word] += 1

        # ограничиваем словарь по частоте
        most_common = sorted(doc_freq.items(), key=lambda x: x[1], reverse=True)
        most_common = most_common[:self.max_features]

        # создаём vocab
        self.vocab = {word: idx for idx, (word, _) in enumerate(most_common)}

        # считаем IDF
        for word, df in most_common:
            self.idf[word] = math.log((total_docs + 1) / (df + 1)) + 1

    def transform(self, corpus):
        """
        возвращает список векторов (list of list)
        """
        vectors = []

        for doc in corpus:
            tf = Counter(doc)
            doc_len = len(doc)

            vector = {}

            for word, count in tf.items():
                if word in self.vocab:
                    idx = self.vocab[word]

                    tf_value = count / doc_len
                    tfidf = tf_value * self.idf[word]

                    vector[idx] = tfidf

            norm = math.sqrt(sum(v * v for v in vector.values()))

            if norm > 0:
                for k in vector:
                    vector[k] /= norm

            vectors.append(vector)

        return vectors

    def fit_transform(self, corpus):
        self.fit(corpus)
        return self.transform(corpus)