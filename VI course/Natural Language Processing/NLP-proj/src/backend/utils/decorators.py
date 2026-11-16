"""Файл, описывающий все используемые декораторы"""

from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Awaitable
import functools

from sqlalchemy import select

from backend.db import SteamProfile


def with_cache(
        func: Callable[..., Awaitable[dict[str, Any]]]
) -> Callable[..., Awaitable[tuple[dict[str, Any], bool]]]:
    """Декоратор получения инфо о Steam-профиле с применением кэширования"""

    @functools.wraps(func)
    async def wrapper(
            self,
            identifier: str,
            *,
            refresh: bool = False
    ) -> tuple[dict[str, Any], bool]:
        """Обертка над функцией"""

        # Определяем тип идентификатора
        kind, value = self.parse_steam_identifier(identifier)

        # Ищем профиль по vanity-URL
        cached = None

        if kind == "vanity":
            cached = await self.session.scalar(
                select(SteamProfile).where(SteamProfile.vanity_url == value)
            )

        # Получаем SteamID
        if kind == "steam_id":
            steam_id = value
        elif cached:
            steam_id = cached.steam_id
        else:
            steam_id = await self.gateway.resolve_vanity_url(value)

        # Если не нашли по vanity-URL, ищем по SteamID
        if cached is None:
            cached = await self.session.scalar(
                select(SteamProfile).where(SteamProfile.steam_id == steam_id)
            )

        # Проверяем срок действия кэша
        now = datetime.now(timezone.utc)
        cached_expiry = cached.expires_data if cached else None

        if cached_expiry and cached_expiry.tzinfo is None:
            cached_expiry = cached_expiry.replace(
                tzinfo=timezone.utc
            )

        if cached and not refresh and cached_expiry and cached_expiry > now:
            cached.cache_hits += 1
            await self.session.commit()
            return cached.profile_data, True

        # Кэша нет или он устарел — вызываем исходную функцию
        profile_data = await func(self, steam_id)

        # Рассчитываем время жизни кэша
        ttl = max(1, self.settings.steam_cache_ttl_hours)
        fetched_at = datetime.now(timezone.utc)
        expires_data = fetched_at + timedelta(hours=ttl)

        # Обновляем существующую запись (если есть)
        if cached:
            if kind == "vanity":
                cached.vanity_url = value

            cached.persona_name = profile_data.get("persona_name")
            cached.profile_url = profile_data.get("profile_url")
            cached.profile_data = profile_data
            cached.expires_data = expires_data
            cached.update_date = fetched_at

        # Создаём новую запись (если нет)
        else:
            cached = SteamProfile(
                steam_id=steam_id,
                vanity_url=value if kind == "vanity" else None,
                persona_name=profile_data.get("persona_name"),
                profile_url=profile_data.get("profile_url"),
                profile_data=profile_data,
                expires_data=expires_data,
            )

            self.session.add(cached)

        await self.session.commit()

        return profile_data, False

    return wrapper
