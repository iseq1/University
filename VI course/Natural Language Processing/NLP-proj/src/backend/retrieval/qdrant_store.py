"""Адаптер векторного хранилища Qdrant"""

from collections.abc import Sequence
from uuid import NAMESPACE_URL, uuid5

from src.backend.core import get_settings
from src.backend.retrieval import RetrievedDocument


class QdrantVectorStore:
    """Асинхронная обертка для коллекции Qdrant, предназначенная для примеров из базы знаний"""


    def __init__(self, client=None, collection_name: str | None = None) -> None:
        self.collection_name = collection_name or get_settings().qdrant_collection
        self._client = client


    def _get_client(self):
        """Получение внутреннего клиента"""

        if self._client is None:
            try:
                from qdrant_client import AsyncQdrantClient
            except ImportError as exc:
                raise RuntimeError(
                    "Установите qdrant-client: poetry install"
                ) from exc

            settings = get_settings()
            self._client = AsyncQdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key.get_secret_value()
                if settings.qdrant_api_key else None,
            )

        return self._client


    async def ensure_collection(self, vector_size: int) -> None:
        """Создание коллекции"""
        from qdrant_client.http import models

        client = self._get_client()
        exists = await client.collection_exists(self.collection_name)

        if not exists:
            await client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE
                ),
            )


    async def upsert(self, documents: Sequence[RetrievedDocument], vectors: Sequence[Sequence[float]]) -> int:
        """Добавление или обновление документов и их векторных представлений"""

        if len(documents) != len(vectors):
            raise ValueError(
                "Количество документов и векторов должно совпадать"
            )

        if not documents:
            return 0

        from qdrant_client.http import models

        await self.ensure_collection(len(vectors[0]))
        points = []

        for document, vector in zip(documents, vectors, strict=True):
            point_id = str(uuid5(NAMESPACE_URL, f"gamer-passport:{document.id}"))
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=list(vector),
                    payload={
                        "document_id": document.id,
                        "source_text": document.source_text,
                        "target_text": document.target_text,
                        "category": document.category,
                    },
                )
            )

        await self._get_client().upsert(
            collection_name=self.collection_name, points=points, wait=True
        )

        return len(points)


    async def search(self, vector: Sequence[float], limit: int = 5) -> list[tuple[RetrievedDocument, float]]:
        """Поиск ближайших векторов и восстановление извлеченных документов"""

        if limit <= 0:
            return []

        response = await self._get_client().query_points(
            collection_name=self.collection_name,
            query=list(vector),
            limit=limit,
            with_payload=True,
        )

        results = []
        for point in response.points:
            payload = point.payload or {}

            if not payload.get("source_text") or not payload.get("target_text"):
                continue

            document = RetrievedDocument(
                id=str(payload.get("document_id", point.id)),
                source_text=payload["source_text"],
                target_text=payload["target_text"],
                category=payload.get("category"),
            )

            results.append((document, float(point.score)))

        return results


    async def close(self) -> None:
        """Закрытие используемого асинхронного клиента Qdrant, если он был создан"""
        if self._client is not None:
            await self._client.close()
