"""Эндпоинты CRUD и импорта для базы знаний и глоссария"""
from __future__ import annotations

import csv
import io

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.db import Session, Glossary, KnowledgeBase, User
from src.backend.api.deps import require_admin, require_editor
from src.backend.api.schemas.admin import KnowledgeItem, GlossaryItem, KnowledgeImport, CSVImport


async_session = Session().get_session


class AdminRouter:
    """API-класс, описывающий endpoint-ы CRUD и импорта для базы знаний и глоссария"""


    def __init__(self):
        self.router = APIRouter(prefix="/api/v1/admin", tags=["administration"])
        self._register_routes()


    def _register_routes(self) -> None:
        """Регистрация endpoint-ов авторизации"""

        self.router.add_api_route(
            "/knowledge-base",
            endpoint=self.get_list_knowledge,
            methods=["GET"],
        )

        self.router.add_api_route(
            "/knowledge-base",
            endpoint=self.add_knowledge,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
        )

        self.router.add_api_route(
            "/knowledge-base/{item_id}",
            endpoint=self.update_knowledge,
            methods=["PUT"],
        )

        self.router.add_api_route(
            "/knowledge-base/{item_id}",
            endpoint=self.delete_knowledge,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )

        self.router.add_api_route(
            "/glossary",
            endpoint=self.get_list_glossary,
            methods=["GET"],
        )

        self.router.add_api_route(
            "/glossary",
            endpoint=self.add_glossary,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
        )

        self.router.add_api_route(
            "/glossary/{item_id}",
            endpoint=self.update_glossary,
            methods=["PUT"],
        )

        self.router.add_api_route(
            "/glossary/{item_id}",
            endpoint=self.delete_glossary,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )

        self.router.add_api_route(
            "/knowledge-base/import",
            endpoint=self.import_knowledge,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
        )

        self.router.add_api_route(
            "/knowledge-base/import-csv",
            endpoint=self.import_knowledge_csv,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
        )


    @staticmethod
    async def get_list_knowledge(
        _: User = Depends(require_editor),
        session: AsyncSession = Depends(async_session)
    ):
        """Получение списка данных из базы знаний"""

        rows = (await session.execute(select(KnowledgeBase).order_by(KnowledgeBase.internal_id).limit(500))).scalars().all()
        return [
            {
                "internal_id": row.internal_id,
                "source_text": row.source_text,
                "target_text": row.target_text,
                "category": row.category
            }
            for row in rows
        ]


    @staticmethod
    async def add_knowledge(
        data: KnowledgeItem,
        _: User = Depends(require_admin),
        session: AsyncSession = Depends(async_session)
    ):
        """Добавить запись в базу знаний"""

        row = KnowledgeBase(**data.model_dump())
        session.add(row); await session.commit(); await session.refresh(row)
        return {
            "internal_id": row.internal_id
        }


    @staticmethod
    async def update_knowledge(
        item_id: int,
        data: KnowledgeItem,
        _: User = Depends(require_admin),
        session: AsyncSession = Depends(async_session)
    ):
        """Обновление записи в базе знаний"""

        row = await session.get(KnowledgeBase, item_id)

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Knowledge item not found"
            )

        for key, value in data.model_dump().items():
            setattr(row, key, value)

        await session.commit()

        return {
            "internal_id": row.internal_id,
            "updated": True
        }


    @staticmethod
    async def delete_knowledge(
        item_id: int,
        _: User = Depends(require_admin),
        session: AsyncSession = Depends(async_session)
    ):
        row = await session.get(KnowledgeBase, item_id)

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Knowledge item not found"
            )

        await session.delete(row); await session.commit()


    @staticmethod
    async def get_list_glossary(
        _: User = Depends(require_editor),
        session: AsyncSession = Depends(async_session)
    ):
        """Получение списка записей из глоссария"""

        rows = (await session.execute(select(Glossary).order_by(Glossary.internal_id).limit(500))).scalars().all()
        return [
            {
                "internal_id": row.internal_id,
                 "term": row.term,
                 "definition": row.definition,
                 "category": row.category
            }
            for row in rows
        ]


    @staticmethod
    async def add_glossary(
        data: GlossaryItem,
        _: User = Depends(require_admin),
       session: AsyncSession = Depends(async_session)
    ):
        """Добавление записи в глоссарий"""

        row = Glossary(**data.model_dump())
        session.add(row); await session.commit(); await session.refresh(row)
        return {
            "internal_id": row.internal_id
        }


    @staticmethod
    async def update_glossary(
        item_id: int,
        data: GlossaryItem,
        _: User = Depends(require_admin),
        session: AsyncSession = Depends(async_session)
    ):
        """Обновление записи в глоссарии"""

        row = await session.get(Glossary, item_id)

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Glossary item not found"
            )

        for key, value in data.model_dump().items():
            setattr(row, key, value)

        await session.commit()

        return {
            "internal_id": row.internal_id,
            "updated": True
        }


    @staticmethod
    async def delete_glossary(
        item_id: int,
        _: User = Depends(require_admin),
        session: AsyncSession = Depends(async_session)
    ):
        """Удаление записи из глоссария"""

        row = await session.get(Glossary, item_id)

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Glossary item not found"
            )

        await session.delete(row); await session.commit()


    @staticmethod
    async def import_knowledge(
        data: KnowledgeImport,
        _: User = Depends(require_admin),
        session: AsyncSession = Depends(async_session)
    ):
        """Импорт базы знаний"""

        inserted = skipped = 0

        for item in data.items:
            exists = await session.scalar(select(KnowledgeBase.internal_id).where(
                KnowledgeBase.source_text == item.source_text,
                KnowledgeBase.target_text == item.target_text
            ))

            if exists is not None:
                skipped += 1
                continue

            session.add(KnowledgeBase(**item.model_dump())); inserted += 1

        await session.commit()

        return {
            "inserted": inserted,
            "skipped_duplicates": skipped
        }


    @staticmethod
    async def import_knowledge_csv(
        data: CSVImport,
        _: User = Depends(require_admin),
        session: AsyncSession = Depends(async_session)
    ):
        """Импорт базы знаний через CSV"""
        try:
            reader = csv.DictReader(io.StringIO(data.csv_text))
            required = {
                "source_text",
                "target_text"
            }

            if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
                raise ValueError(
                    "CSV headers must include source_text,target_text; category is optional"
                )

            rows = list(reader)
            if not rows or len(rows) > 1000:
                raise ValueError(
                    "CSV must contain between 1 and 1000 data rows"
                )

            inserted = skipped = 0
            for raw in rows:
                item = KnowledgeItem(
                    source_text=raw.get("source_text", "").strip(),
                    target_text=raw.get("target_text", "").strip(),
                    category=(raw.get("category") or None)
                )

                exists = await session.scalar(select(KnowledgeBase.internal_id).where(
                    KnowledgeBase.source_text == item.source_text,
                    KnowledgeBase.target_text == item.target_text
                ))

                if exists is not None:
                    skipped += 1
                else:
                    session.add(KnowledgeBase(**item.model_dump())); inserted += 1

            await session.commit()

            return {
                "inserted": inserted,
                "skipped_duplicates": skipped
            }

        except (ValueError, TypeError) as exc:
            await session.rollback()
            raise HTTPException(
                status_code=422,
                detail=str(exc)
            ) from exc
