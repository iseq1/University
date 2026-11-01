"""Вспомогательные средства для загрузки базы знаний и создания гибридного поискового механизма"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.db import KnowledgeBase
from src.backend.retrieval import HybridRetriever, RetrievedDocument


class RetrivalService:
    """Сервиса для взаимодействия с механизмом гибридного поиска"""

    def __init__(self): pass


    @staticmethod
    async def load_knowledge_documents(session: AsyncSession) -> list[RetrievedDocument]:
        """Загрузка примеры из базы знаний"""
        result = await session.execute(select(KnowledgeBase).order_by(KnowledgeBase.internal_id))
        return [
            RetrievedDocument(
                id=str(row.internal_id),
                source_text=row.source_text,
                target_text=row.target_text,
                category=row.category,
            )
            for row in result.scalars().all()
        ]


    async def build_retriever(self, session: AsyncSession) -> HybridRetriever:
        """Создание гибридного поискового механизма"""
        documents = await self.load_knowledge_documents(session)

        if not documents:
            raise ValueError(
                "База знаний пуста. Сначала выполните scripts/import_data.py"
            )

        return HybridRetriever(documents)
