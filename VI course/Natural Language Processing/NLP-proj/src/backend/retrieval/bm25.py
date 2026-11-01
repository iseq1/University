"""Лексический поиск BM25"""

import re
from collections.abc import Sequence

from src.backend.retrieval import RetrievedDocument

_TOKEN_RE = re.compile(r"[\w+#.]+", flags=re.UNICODE)


def tokenize(text: str) -> list[str]:
    """Токенизация русского и английского текста"""
    return [token.casefold() for token in _TOKEN_RE.findall(text)]


class BM25Retriever:
    """Извлечение примеров с использованием BM25O на основе исходных текстов"""


    def __init__(
        self,
        documents: Sequence[RetrievedDocument],
        *,
        k1: float = 1.5,
        b: float = 0.75
    ) -> None:
        self.documents = list(documents)
        self._tokenized = [tokenize(doc.source_text) for doc in self.documents]
        self._index = None
        self._fallback_params = (k1, b)

        if self.documents:
            try:
                from rank_bm25 import BM25Okapi
                self._index = BM25Okapi(self._tokenized, k1=k1, b=b)

            except ImportError:
                self._index = None


    def _fallback_scores(self, query_tokens: list[str]) -> list[float]:
        """Упрощенная реализация BM25 в роли fallback"""
        import math
        from collections import Counter

        k1, b = self._fallback_params
        if not query_tokens:
            return [0.0] * len(self._tokenized)

        doc_count = len(self._tokenized)
        average_length = sum(map(len, self._tokenized)) / max(doc_count, 1)

        document_frequency = {
            token: sum(token in set(doc) for doc in self._tokenized)
            for token in set(query_tokens)
        }

        result = []
        for document in self._tokenized:
            frequencies = Counter(document)
            score = 0.0

            for token in query_tokens:
                frequency = frequencies[token]

                if not frequency:
                    continue

                df = document_frequency[token]
                idf = math.log(1 + (doc_count - df + 0.5) / (df + 0.5))
                denominator = frequency + k1 * (1 - b + b * len(document) / max(average_length, 1e-9))
                score += idf * frequency * (k1 + 1) / denominator
            result.append(score)

        return result


    def search(self, query: str, limit: int = 5) -> list[tuple[RetrievedDocument, float]]:
        """Поиск наиболее подходящего лексического совпадения вместе с их оценками по алгоритму BM25"""

        if not self.documents or limit <= 0:
            return []

        tokens = tokenize(query)
        if self._index is not None:
            scores = self._index.get_scores(tokens)
        else:
            scores = self._fallback_scores(tokens)

        indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

        return [
            (self.documents[i], float(scores[i]))
            for i in indices[:limit]
            if scores[i] > 0
        ]
