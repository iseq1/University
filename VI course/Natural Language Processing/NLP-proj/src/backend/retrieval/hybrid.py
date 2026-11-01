"""Гибридный поиск с использованием метода взаимного рангового слияния (RRF)"""

from collections import defaultdict
from collections.abc import Sequence

from src.backend.retrieval import BM25Retriever, RetrievedDocument, SentenceTransformerEmbedder, QdrantVectorStore


class HybridRetriever:
    """Объединение лексического ранжирования BM25 и семантического ранжирования Qdrant с помощью RRF"""

    def __init__(
        self,
        documents: Sequence[RetrievedDocument],
        embedder: SentenceTransformerEmbedder | None = None,
        vector_store: QdrantVectorStore | None = None,
        *,
        rrf_k: int = 60
    ) -> None:

        if rrf_k <= 0:
            raise ValueError(
                "rrf_k должен быть положительным"
            )

        self.documents = list(documents)
        self.embedder = embedder or SentenceTransformerEmbedder()
        self.vector_store = vector_store or QdrantVectorStore()
        self.bm25 = BM25Retriever(self.documents)
        self.rrf_k = rrf_k


    async def index(self, batch_size: int = 64) -> int:
        """Кодировка и загрузка документы"""

        if batch_size <= 0:
            raise ValueError(
                "batch_size должен быть положительным"
            )

        indexed = 0
        for start in range(0, len(self.documents), batch_size):
            batch = self.documents[start:start + batch_size]
            vectors = self.embedder.encode([doc.source_text for doc in batch])
            indexed += await self.vector_store.upsert(batch, vectors)

        return indexed


    @staticmethod
    def reciprocal_rank_fusion(
        rankings: Sequence[Sequence[tuple[RetrievedDocument, float]]],
        *,
        k: int = 60
    ) -> list[tuple[RetrievedDocument, float]]:
        """Объединение ранжированных списков"""

        if k <= 0:
            raise ValueError(
                "k должен быть положительным"
            )

        scores: dict[str, float] = defaultdict(float)
        docs: dict[str, RetrievedDocument] = {}
        for ranking in rankings:
            seen_in_ranking: set[str] = set()

            for rank, (document, _) in enumerate(ranking, start=1):
                if document.id in seen_in_ranking:
                    continue
                seen_in_ranking.add(document.id)
                docs[document.id] = document
                scores[document.id] += 1.0 / (k + rank)

        return sorted(
            ((docs[doc_id], score) for doc_id, score in scores.items()),
            key=lambda item: item[1],
            reverse=True,
        )


    async def search(self, query: str, limit: int = 5, candidate_limit: int | None = None ) -> list[tuple[RetrievedDocument, float]]:
        """Поиск лучших результаты"""

        if not query.strip() or limit <= 0:
            return []

        candidates = candidate_limit or max(limit * 3, 10)
        lexical = self.bm25.search(query, candidates)
        query_vector = self.embedder.encode([query])[0]
        semantic = await self.vector_store.search(query_vector, candidates)

        return self.reciprocal_rank_fusion(
            rankings=[lexical, semantic],
            k=self.rrf_k
        )[:limit]
