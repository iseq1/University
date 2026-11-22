"""Получение профиля Steam, его сохранение и кэширование с использованием TTL"""

from urllib.parse import urlparse
from typing import Any
import re

from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.core import get_settings, SteamIdentifierError
from src.backend.gateways import SteamGateway
from src.backend.utils import with_cache


STEAM_ID64_RE = re.compile(r"^7656119\d{10}$")
VANITY_RE = re.compile(r"^[A-Za-z0-9_-]{2,64}$")


class SteamProfileService:
    """Сервис для взаимодействия со Steam"""


    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.settings = get_settings()
        self.gateway = SteamGateway()


    async def _get_steam_profile_info(self, steam_id: str):
        """Получение базовых данных о Steam-профиле"""

        player = await self.gateway.get_player_summary(steam_id=steam_id)
        games, games_available = await self.gateway.get_owned_games(steam_id=steam_id)
        recent, recent_available = await self.gateway.get_recently_played_games(steam_id=steam_id)

        return self.normalize_profile_info(
            player=player,
            games=games,
            recent_games=recent,
            games_available=games_available,
            recent_games_available=recent_available,
        )


    @with_cache
    async def get_steam_profile_info(self, steam_id: str) -> dict[str, Any]:
        """Получение данных о Steam-профиле"""
        return await self._get_steam_profile_info(
            steam_id=steam_id
        )

    @staticmethod
    def parse_steam_identifier(value: str) -> tuple[str, str]:
        """Парсинг идентификатора Steam"""

        candidate = value.strip()
        if STEAM_ID64_RE.fullmatch(candidate):
            return "steam_id", candidate

        if "://" not in candidate:
            candidate = f"https://{candidate}"

        parsed = urlparse(candidate)
        if parsed.scheme not in {"http", "https"} or parsed.hostname not in {
            "steamcommunity.com", "www.steamcommunity.com"
        }:
            raise SteamIdentifierError(
                "Укажите SteamID64 или ссылку на steamcommunity.com"
            )

        parts = [part for part in parsed.path.split("/") if part]

        if len(parts) != 2 or parts[0] not in {"id", "profiles"}:
            raise SteamIdentifierError(
                "Ожидается ссылка вида /id/username или /profiles/SteamID64"
            )

        if parts[0] == "profiles":
            if not STEAM_ID64_RE.fullmatch(parts[1]):
                raise SteamIdentifierError(
                    "В ссылке /profiles/ должен быть корректный SteamID64"
                )

            return "steam_id", parts[1]

        if not VANITY_RE.fullmatch(parts[1]):
            raise SteamIdentifierError(
                "Некорректный vanity URL Steam-профиля"
            )

        return "vanity", parts[1]


    @staticmethod
    def normalize_profile_info(
        player: dict[str, Any],
        games: list[dict[str, Any]],
        recent_games: list[dict[str, Any]],
        *,
        games_available: bool,
        recent_games_available: bool,
    ) -> dict[str, Any]:
        """Формирование компактного профильного пакета данных"""
        return {
            "steam_id": str(player.get("steamid", "")),
            "persona_name": player.get("personaname"),
            "profile_url": player.get("profileurl"),
            "avatar_url": player.get("avatarfull") or player.get("avatarmedium"),
            "persona_state": player.get("personastate"),
            "community_visibility_state": player.get("communityvisibilitystate"),
            "profile_state": player.get("profilestate"),
            "created_at_unix": player.get("timecreated"),
            "country_code": player.get("loccountrycode"),
            "games_available": games_available,
            "recent_games_available": recent_games_available,
            "games_count": len(games),
            "games": [
                {
                    "app_id": game.get("appid"),
                    "name": game.get("name"),
                    "playtime_forever": float(game.get("playtime_forever")) / 60 if game.get("playtime_forever") else 0,
                    "playtime_2weeks": float(game.get("playtime_2weeks")) / 60 if game.get("playtime_2weeks") else 0,
                    "img_icon_url": game.get("img_icon_url"),
                }
                for game in games
            ],
            "recent_games": [
                {
                    "app_id": game.get("appid"),
                    "name": game.get("name"),
                    "playtime_2weeks": float(game.get("playtime_2weeks")) / 60 if game.get("playtime_2weeks") else 0,
                    "playtime_forever": float(game.get("playtime_forever")) / 60 if game.get("playtime_forever") else 0,    
                }
                for game in recent_games
            ],
        }
