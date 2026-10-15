"""Управление асинхронным движком и сессиями SQLAlchemy"""

from collections.abc import AsyncGenerator
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.backend.core import get_settings


class Session:
    """Класс, описывающий взаимодействие с сессией"""

    def __init__(self):
        self.settings = get_settings()


    @lru_cache(maxsize=1)
    def get_engine(self) -> AsyncEngine:
        """Создание и кэширование асинхронного движка SQLAlchemy"""
        return create_async_engine(
            self.settings.database_url,
            echo=self.settings.debug,
            pool_pre_ping=True,
        )

    @lru_cache(maxsize=1)
    def get_session_factory(self) -> async_sessionmaker[AsyncSession]:
        """Создание и кэширование асинхронной фабрики сессий"""
        return async_sessionmaker(
            bind=self.get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )


    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Генератор открытой БД-сессии"""
        async with self.get_session_factory()() as session:
            yield session


    async def init_db(self) -> None:
        """Создание всех таблиц при условии их отсутствия"""
        from src.backend.db.models import Base

        async with self.get_engine().begin() as connection:
            await connection.run_sync(Base.metadata.create_all)


    async def close_db(self) -> None:
        """Закрытие БД-сессии"""
        if self.get_engine.cache_info().currsize:
            await self.get_engine().dispose()
            self.get_session_factory.cache_clear()
            self.get_engine.cache_clear()
