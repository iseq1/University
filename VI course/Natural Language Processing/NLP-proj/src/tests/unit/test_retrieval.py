"""Модульные тесты для компонентов лексического, векторного и гибридного поиска"""

import pytest

from src.backend.retrieval import HybridRetriever, RetrievedDocument, BM25Retriever, tokenize


class FakeEmbedder:
    def encode(self, texts):
        return [[float(len(text)), 1.0] for text in texts]


class FakeVectorStore:
    def __init__(self, results=None):
        self.results = results or []
        self.upserted = []

    async def upsert(self, documents, vectors):
        self.upserted.extend(zip(documents, vectors))
        return len(documents)

    async def search(self, vector, limit=5):
        return self.results[:limit]


@pytest.fixture

def documents():
    return [
        RetrievedDocument("1", "Dota 2 competitive matches", "Игрок любит Dota 2", "moba"),
        RetrievedDocument("2", "Counter-Strike 2 shooter", "Игрок любит CS2", "shooter"),
        RetrievedDocument("3", "Stardew Valley farming game", "Игрок любит фермы", "simulator"),
    ]


def test_tokenize_handles_russian_and_game_names():
    assert tokenize("Dota 2 и Counter-Strike 2") == ["dota", "2", "и", "counter", "strike", "2"]


def test_bm25_returns_relevant_document(documents):
    results = BM25Retriever(documents).search("Dota 2", limit=2)
    assert results
    assert results[0][0].id == "1"


def test_bm25_empty_query_returns_empty(documents):
    assert BM25Retriever(documents).search("", limit=3) == []


def test_rrf_promotes_document_ranked_by_both_methods(documents):
    fused = HybridRetriever.reciprocal_rank_fusion([
        [(documents[0], 10), (documents[1], 8)],
        [(documents[1], 0.9), (documents[0], 0.8)],
    ])
    assert fused[0][0].id in {"1", "2"}
    assert len(fused) == 2
    assert fused[0][1] == pytest.approx(fused[1][1])


def test_rrf_rejects_invalid_k(documents):
    with pytest.raises(ValueError):
        HybridRetriever.reciprocal_rank_fusion([[(documents[0], 1)]], k=0)


def test_hybrid_search_combines_bm25_and_vector_results(documents):
    vector_store = FakeVectorStore([(documents[1], 0.99), (documents[2], 0.8)])
    retriever = HybridRetriever(documents, FakeEmbedder(), vector_store)
    results = __import__("asyncio").run(retriever.search("Dota 2", limit=3))
    assert len(results) == 3
    assert {item.id for item, _ in results} == {"1", "2", "3"}


def test_index_uploads_in_batches(documents):
    vector_store = FakeVectorStore()
    retriever = HybridRetriever(documents, FakeEmbedder(), vector_store)
    count = __import__("asyncio").run(retriever.index(batch_size=2))
    assert count == 3
    assert len(vector_store.upserted) == 3


def test_index_rejects_non_positive_batch_size(documents):
    retriever = HybridRetriever(documents, FakeEmbedder(), FakeVectorStore())
    with pytest.raises(ValueError):
        __import__("asyncio").run(retriever.index(batch_size=0))


def test_rrf_rewards_document_ranked_first_by_both_sources(documents):
    fused = HybridRetriever.reciprocal_rank_fusion([
        [(documents[0], 0.1), (documents[1], 100)],
        [(documents[0], 0.2), (documents[2], 100)],
    ])
    assert fused[0][0].id == "1"
