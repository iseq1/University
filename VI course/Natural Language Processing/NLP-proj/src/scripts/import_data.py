"""Импорт сгенерированных JSON-наборов данных в асинхронную БД"""

from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
from typing import Any
import logging
import asyncio
import json
import sys

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.db import Glossary, KnowledgeBase, Session


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATA_DIR = ROOT / "data" / "generated"
LOGGER = logging.getLogger(__name__)


class DataImporter:
    """Класс, описывающий логику импорта данных в БД"""


    def __init__(self):
        self.parser = ArgumentParser(description=__doc__)
        self.session = Session()


    @staticmethod
    def load_json_records(path: Path) -> list[dict[str, Any]]:
        """Загрузка JSON-массива записей"""

        if not path.exists():
            raise FileNotFoundError(
                f"Файл данных не найден: {path}. Сначала запустите generate_data.py"
            )

        data = json.loads(path.read_text(encoding="utf-8"))

        if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
            raise ValueError(
                f"Ожидался JSON-массив объектов: {path}"
            )

        return data


    @staticmethod
    def _clean_text(value: Any, field: str, row_number: int) -> str:
        """Чистка текста"""

        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Запись {row_number}: поле {field!r} должно быть непустой строкой"
            )

        return value.strip()


    def normalize_knowledge_records(self, records: list[dict[str, Any]]) -> list[dict[str, str | None]]:
        """Проверка записи и сортировка дублей"""
        result = []
        seen = set()

        for row_number, record in enumerate(iterable=records, start=1):
            source_text = self._clean_text(
                value=record.get("source_text"),
                field="source_text",
                row_number=row_number
            )

            target_text = self._clean_text(
                value=record.get("target_text"),
                field="target_text",
                row_number=row_number
            )

            key = source_text.casefold()
            if key in seen:
                continue
            seen.add(key)

            category = record.get("category")
            result.append({
                "source_text": source_text,
                "target_text": target_text,
                "category": category.strip() if isinstance(category, str) and category.strip() else None
            })

        return result


    def normalize_glossary_records(self, records: list[dict[str, Any]]) -> list[dict[str, str | None]]:
        """Проверка записи в глоссарии и сортировка дубликатов"""

        result = []
        seen = set()

        for row_number, record in enumerate(iterable=records, start=1):
            term = self._clean_text(
                value=record.get("term"),
                field="term",
                row_number=row_number
            )

            definition = self._clean_text(
                value=record.get("definition"),
                field="definition",
                row_number=row_number
            )

            key = term.casefold()
            if key in seen:
                continue
            seen.add(key)

            category = record.get("category")
            result.append({
                "term": term,
                "definition": definition,
                "category": category.strip() if isinstance(category, str) and category.strip() else None
            })

        return result


    async def import_knowledge_base(self, session: AsyncSession, records: list[dict[str, Any]]) -> int:
        """Добавление уникальных примеров знаний"""

        normalized = self.normalize_knowledge_records(records=records)

        existing_result = await session.execute(select(KnowledgeBase.source_text))
        existing = {value.casefold() for value in existing_result.scalars().all()}

        new_records = [
            row for row in normalized
            if row["source_text"].casefold() not in existing
        ]

        session.add_all([KnowledgeBase(**row) for row in new_records])
        await session.commit()

        LOGGER.info(
            "Импортировано записей базы знаний: %d; пропущено: %d",
            len(new_records), len(records) - len(new_records)
        )

        return len(new_records)


    async def import_glossary(self, session: AsyncSession, records: list[dict[str, Any]]) -> int:
        """Добавление уникальных терминов из глоссария"""

        normalized = self.normalize_glossary_records(records=records)

        existing_result = await session.execute(select(Glossary.term))
        existing = {value.casefold() for value in existing_result.scalars().all()}

        new_records = [
            row for row in normalized
            if row["term"].casefold() not in existing
        ]

        session.add_all([Glossary(**row) for row in new_records])
        await session.commit()

        LOGGER.info(
            "Импортировано терминов глоссария: %d; пропущено: %d",
            len(new_records), len(records) - len(new_records)
        )

        return len(new_records)


    async def run_import(self, data_dir: Path = DATA_DIR) -> dict[str, int]:
        """Инициализация таблиц и импорт обучающей базы знаний и глоссария"""

        await self.session.init_db()
        factory = self.session.get_session_factory()

        async with factory() as session:
            kb_records = self.load_json_records(path=data_dir / "knowledge_base_train.json")
            glossary_records = self.load_json_records(path=data_dir / "glossary.json")

            kb_count = await self.import_knowledge_base(
                session=session,
                records=kb_records
            )

            glossary_count = await self.import_glossary(
                session=session,
                records=glossary_records
            )

        return {
            "knowledge_base_inserted": kb_count,
            "glossary_inserted": glossary_count
        }


    async def run(self, data_dir: Path) -> None:
        """Запуск импорта"""
        counts = await self.run_import(data_dir=data_dir)
        for name, count in counts.items():
            print(f"{name}: {count}")


    def main(self):
        """Основной метод класса"""
        self.parser.add_argument("--data-dir", type=Path, default=DATA_DIR)
        args = self.parser.parse_args()

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s"
        )

        asyncio.run(self.run(args.data_dir))


if __name__ == "__main__":
    DataImporter().main()
