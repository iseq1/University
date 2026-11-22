"""Асинхронный клиент для публичных эндпоинтов профиля в Steam Web API"""

from typing import Any

import httpx

from src.backend.core import SteamAPIError


class SteamAPIClient:
    """Клиент взаимодействия с SteamAPI"""

    def __init__(self, api_key: str, base_url: str, timeout: float = 15.0) -> None:

        if not api_key:
            raise ValueError("STEAM_API_KEY не указан в конфигурации проекта")

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout


    async def call(self, interface: str, method: str, *, version: str = "v0001", **params: Any) -> dict[str, Any]:
        """GET запрос к сервису через SteamAPI"""

        url = f"{self.base_url}/{interface}/{method}/{version}/"
        query = {
            "key": self.api_key,
            "format": "json",
            **params
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=query)
                response.raise_for_status()
                payload = response.json()

        except httpx.TimeoutException as exc:
            raise SteamAPIError(
                "Истекло время ожидания запроса к Steam API"
            ) from exc

        except httpx.HTTPStatusError as exc:
            raise SteamAPIError(
                f"Steam API вернул HTTP-ответ {exc.response.status_code}"
            ) from exc

        except (httpx.HTTPError, ValueError) as exc:
            raise SteamAPIError(
                "Не удалось связаться с API Steam"
            ) from exc

        if not isinstance(payload, dict):
            raise SteamAPIError(
                "SteamAPI вернул некорректный ответ"
            )

        return payload
