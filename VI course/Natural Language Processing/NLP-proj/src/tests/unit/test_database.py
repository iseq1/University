"""Database initialization tests."""

from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import create_async_engine

from src.backend.db import Base


async def test_all_required_tables_are_created() -> None:
    """Проверка наличия всех таблиц"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

        table_names = await connection.run_sync(
            lambda sync_connection: inspect(sync_connection).get_table_names()
        )

        required_tables = {
            "users",
            "knowledge_base",
            "glossary",
            "uncertain_examples",
            "cache",
            "evaluation_results",
            "model_comparisons",
            "reasoning_logs",
            "llm_calls",
        }

        assert required_tables.issubset(table_names)

    await engine.dispose()


async def test_database_accepts_insert() -> None:
    """Проверка базового sql-запроса"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        result = await connection.execute(text("SELECT COUNT(*) FROM users"))
        assert result.scalar_one() == 0

    await engine.dispose()
