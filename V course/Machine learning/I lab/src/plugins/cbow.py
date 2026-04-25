import numpy as np
from collections import Counter
from src.plugins.dataset_preprocessor import DatasetPreprocessor
from src.plugins.text_preprocessor import TextPreprocessor

class CBOW:
    def __init__(self, corpus, window_size=2, embedding_dim=100, min_count=5):
        self.corpus = corpus
        self.window_size = window_size
        self.embedding_dim = embedding_dim
        self.min_count = min_count

        self.vocab = {}
        self.id2word = {}
        self.pairs = []

        self.W1 = None
        self.W2 = None

        self._build_vocab()
        self._generate_pairs()
        self._init_weights()

    def _build_vocab(self):
        """создание словаря"""
        all_tokens = [word for doc in self.corpus for word in doc]
        counter = Counter(all_tokens)

        filtered_words = [word for word, c in counter.items() if c >= self.min_count]
        self.vocab = {word: i for i, word in enumerate(filtered_words)}
        self.id2word = {i: w for w, i in self.vocab.items()}

        self.vocab_size = len(self.vocab)
        print("Vocab size:", self.vocab_size)

    def _generate_pairs(self):
        """создание пар"""
        for doc in self.corpus:
            ids = [self.vocab[w] for w in doc if w in self.vocab]

            for i, target in enumerate(ids):
                context = [
                    ids[j] for j in range(max(0, i - self.window_size), min(len(ids), i + self.window_size + 1)) if j != i
                ]
                if context:
                    self.pairs.append((context, target))

        print("Pairs:", len(self.pairs))

    def _init_weights(self):
        """инитим веса"""
        self.W1 = np.random.randn(self.vocab_size, self.embedding_dim) * 0.01
        self.W2 = np.random.randn(self.embedding_dim, self.vocab_size) * 0.01

    @staticmethod
    def softmax(x):
        """функция софтмакс"""
        x = x - np.max(x)
        exp = np.exp(x)
        return exp / np.sum(exp)

    def train(self, epochs=10, lr=0.05, limit_pairs=None):
        for epoch in range(epochs):
            loss = 0
            pairs_to_use = self.pairs if limit_pairs is None else self.pairs[:limit_pairs]

            for context, target in pairs_to_use:
                # forward
                h = np.mean(self.W1[context], axis=0)
                u = np.dot(self.W2.T, h)
                y_pred = self.softmax(u)

                # loss
                loss += -np.log(y_pred[target] + 1e-9)

                # backward
                e = y_pred.copy()
                e[target] -= 1

                dW2 = np.outer(h, e)
                dW1 = np.dot(self.W2, e) / len(context)

                # update
                for idx in context:
                    self.W1[idx] -= lr * dW1
                self.W2 -= lr * dW2

            print(f"Epoch {epoch + 1}, Loss: {loss}")

    @staticmethod
    def cosine_sim(a, b):
        """считаем схожесть"""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def most_similar(self, word, top_n=5):
        if word not in self.vocab:
            return []

        w_vec = self.W1[self.vocab[word]]
        sims = [(w, self.cosine_sim(w_vec, self.W1[i])) for w, i in self.vocab.items()]
        sims = sorted(sims, key=lambda x: x[1], reverse=True)
        return sims[1:top_n + 1]

    def analogy(self, a, b, c, top_n=5):
        if a not in self.vocab or b not in self.vocab or c not in self.vocab:
            return []

        vec = self.W1[self.vocab[a]] - self.W1[self.vocab[b]] + self.W1[self.vocab[c]]
        sims = [(w, self.cosine_sim(vec, self.W1[i])) for w, i in self.vocab.items() if w not in [a, b, c]]
        sims = sorted(sims, key=lambda x: x[1], reverse=True)
        return sims[:top_n]


if __name__ == "__main__":
    # Подготовка корпуса
    ds = TextPreprocessor.get_dataset()
    tokenized_texts = DatasetPreprocessor.get_tokens(dataset=ds)
    corpus = tokenized_texts[:10000]

    # Создание модели
    cbow_model = CBOW(corpus=corpus, window_size=2, embedding_dim=100, min_count=5)

    # Обучение
    cbow_model.train(epochs=5, lr=0.05, limit_pairs=100000)

    # Анализ векторов
    print("\n--- Similar words ---")
    print("game:", cbow_model.most_similar("game"))
    print("good:", cbow_model.most_similar("good"))

    print("\n--- Analogies ---")
    print("good - bad + terrible:", cbow_model.analogy("good", "bad", "terrible"))
    print("fun - boring + interesting:", cbow_model.analogy("fun", "boring", "interesting"))
    print("easy - hard + difficult:", cbow_model.analogy("easy", "hard", "difficult"))
    print("fast - slow + quick:", cbow_model.analogy("fast", "slow", "quick"))
    print("like - hate + love:", cbow_model.analogy("like", "hate", "love"))