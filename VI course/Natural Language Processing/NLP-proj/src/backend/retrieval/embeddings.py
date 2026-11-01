"""Модель эмбеддингов Lazy Sentence Transformers"""

from functools import lru_cache
from typing import Sequence

from src.backend.core import get_settings


class SentenceTransformerEmbedder:
    """Кодировка текста с помощью модели SentenceTransformer"""


    def __init__(self, model_name: str | None = None) -> None:
        self.model_name = model_name or get_settings().embedding_model
        self._model = None


    def _get_model(self):
        """Получение эмбеддинг-модели"""

        if self._model is None:

            try:
                from sentence_transformers import SentenceTransformer

            except ImportError as exc:
                raise RuntimeError(
                    "Для векторизации установите зависимости: poetry install"
                ) from exc

            self._model = SentenceTransformer(self.model_name)

        return self._model


    def encode(self, texts: Sequence[str]) -> list[list[float]]:
        """Получение нормализованных эмбеддингов в виде списков"""

        if not texts:
            return []

        vectors = self._get_model().encode(
            list(texts),
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return vectors.tolist()


@lru_cache(maxsize=1)
def get_embedder() -> SentenceTransformerEmbedder:
    """Получение обертки модели с отложенным встраиванием"""
    return SentenceTransformerEmbedder()
