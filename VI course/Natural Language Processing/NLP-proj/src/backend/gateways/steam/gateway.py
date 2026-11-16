from functools import lru_cache
from typing import Any


from backend.gateways.steam.client import SteamAPIClient, SteamAPIError
from backend.core import get_settings


class SteamGateway:
    """Шлюз взаимодействия с SteamAPI"""

    def __init__(self):

        self.settings = get_settings()
        self.client = SteamAPIClient(
            api_key=self.settings.steam_api_key.get_secret_value(),
            base_url=self.settings.steam_api_base_url,
            timeout=self.settings.steam_api_timeout,
        )


    async def resolve_vanity_url(self, vanity_url: str) -> str:
        """Получение SteamId по ссылке на Steam-профиль"""

        payload = await self.client.call(
            interface=self.settings.steam_user_interface,
            method=self.settings.steam_resolve_vanity_method,
            vanityurl=vanity_url
        )

        response = payload.get("response", {})
        if response.get("success") != 1 or not response.get("steamid"):
            raise SteamAPIError(
                "URL-адрес профиля Steam не найден"
            )

        return str(response["steamid"])


    async def get_player_summary(self, steam_id: str) -> dict[str, Any]:
        """Получение summary по профилю Steam"""

        payload = await self.client.call(
            interface=self.settings.steam_user_interface,
            method=self.settings.steam_player_summaries_method,
            version="v0002",
            steamids=steam_id
        )

        players = payload.get("response", {}).get("players", [])
        if not players:
            raise SteamAPIError(
                "Профиль Steam не найден или недоступен"
            )

        return players[0]


    async def get_owned_games(self, steam_id: str) -> tuple[list[dict[str, Any]], bool]:
        """Получение библиотеки пользователя"""

        payload = await self.client.call(
            interface=self.settings.steam_player_service_interface,
            method=self.settings.steam_owned_games_method,
            steamid=steam_id,
            include_appinfo=1,
            include_played_free_games=1,
        )

        response = payload.get("response", {})
        if "games" not in response:
            return [], False

        return response.get("games") or [], True


    async def get_recently_played_games(self, steam_id: str) -> tuple[list[dict[str, Any]], bool]:
        """Получение последней игровой активности пользователя"""

        payload = await self.client.call(
            interface=self.settings.steam_player_service_interface,
            method=self.settings.steam_recently_played_games_method,
            steamid=steam_id,
            count=10
        )

        response = payload.get("response", {})
        if "games" not in response:
            return [], False

        return response.get("games") or [], True


@lru_cache(maxsize=1)
def get_llm_gateway() -> SteamGateway:
    """Получение SteamAPI-шлюза"""
    return SteamGateway()
