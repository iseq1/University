"""Создание/обновление векторного индекса Qdrant на основе базы знаний"""

from __future__ import annotations

from pathlib import Path
import logging
import asyncio
import sys

from src.backend.db import Session
from src.backend.retrieval import get_embedder, QdrantVectorStore, RetrivalService
from src.scripts import BaseScript


LOGGER = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class IndexKnowledgeBase(BaseScript):
    """Класс, описывающий создание векторного индекса Qdrant"""

    def __init__(self):
        super().__init__()
        self.session = Session()
        self.retrival_service = RetrivalService()


    async def run_index(self, batch_size: int = 64) -> int | None:
        """Загрузка записи и вставка их эмбеддинги в Qdrant"""

        if batch_size <= 0:
            raise ValueError(
                "batch_size должен быть положительным"
            )

        factory = self.session.get_session_factory()

        async with factory() as session:
            documents = await self.retrival_service.load_knowledge_documents(session)

        if not documents:
            await self.session.close_db()
            raise ValueError(
                "База знаний пуста. Сначала выполните scripts/import_data.py"
            )

        embedder = get_embedder()
        store = QdrantVectorStore()
        indexed = 0

        try:
            for start in range(0, len(documents), batch_size):
                batch = documents[start:start + batch_size]
                vectors = embedder.encode([doc.source_text for doc in batch])
                indexed += await store.upsert(batch, vectors)
        finally:
            await store.close()
            await self.session.close_db()

        return indexed


    def main(self) -> None:
        self.parser.add_argument("--batch-size", type=int, default=64)
        args = self.parser.parse_args()

        if args.batch_size <= 0:
            self.parser.error("--batch-size должен быть положительным")

        logging.basicConfig(level=logging.INFO)

        count = asyncio.run(self.run_index(batch_size=args.batch_size))
        LOGGER.info("Проиндексировано документов в Qdrant: %d", count)


if __name__ == "__main__":
    IndexKnowledgeBase().main()
