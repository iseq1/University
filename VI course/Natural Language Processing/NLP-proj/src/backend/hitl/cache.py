"""Кэш генерации с поддержкой базы данных, учётом попаданий и опциональным временем жизни (TTL)"""

from datetime import datetime, timedelta, timezone
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.db import Cache

DEFAULT_TTL_HOURS = 24


class CacheHandler:

    def __init__(self):
        pass


    @staticmethod
    def is_expired(
        created_at: datetime,
        *,
        now: datetime | None = None,
        ttl_hours: int = DEFAULT_TTL_HOURS
    ) -> bool:
        """Проверка необходимости кэша"""

        now = now or datetime.now(timezone.utc)
        created = created_at.replace(tzinfo=timezone.utc) if created_at.tzinfo is None else created_at

        return created + timedelta(hours=ttl_hours) <= now


    @staticmethod
    async def get_cached(
        session: AsyncSession,
        key: str,
        *,
        ttl_hours: int = DEFAULT_TTL_HOURS
    ) -> str | None:
        """Получение кэша"""

        entry = await session.scalar(select(Cache).where(Cache.input_key == key))

        if entry is None:
            return None

        if CacheHandler.is_expired(entry.load_date, ttl_hours=ttl_hours):
            await session.delete(entry)
            await session.commit()
            return None

        entry.hits += 1
        await session.commit()

        return entry.output


    @staticmethod
    async def put_cached(session: AsyncSession, key: str, output: str) -> None:
        """Записать кэш"""

        entry = await session.scalar(select(Cache).where(Cache.input_key == key))

        if entry is None:
            session.add(Cache(input_key=key, output=output, hits=0))
        else:
            entry.output = output
            entry.hits = 0
            entry.load_date = datetime.now(timezone.utc)

        await session.commit()


    @staticmethod
    async def clear_expired(session: AsyncSession, *, ttl_hours: int = DEFAULT_TTL_HOURS) -> int:
        """Чистка просроченного кэша"""

        cutoff = datetime.now(timezone.utc) - timedelta(hours=ttl_hours)
        result = await session.execute(delete(Cache).where(Cache.load_date < cutoff))
        await session.commit()

        return getattr(result, "rowcount", 0) or 0
