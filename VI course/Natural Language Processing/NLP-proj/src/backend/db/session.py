"""Управление асинхронным движком и сессиями SQLAlchemy"""

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.backend.core import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Генератор открытой БД-сессии"""
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    """Создание всех таблиц при условии их отсутствия"""
    from src.backend.db.models import Base

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Закрытие БД-сессии"""
    await engine.dispose()
