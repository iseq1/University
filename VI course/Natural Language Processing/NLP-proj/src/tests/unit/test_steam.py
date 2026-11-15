"""Модульные тесты взаимодействия с Steam"""

import pytest

from src.backend.service.steam import SteamProfileService
from src.backend.gateways.steam import SteamGateway
from src.backend.gateways.steam.client import SteamAPIError
from src.backend.core import SteamIdentifierError

from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def steam_gateway() -> SteamGateway:
    """Создание SteamGateway с замоканным API-клиентом."""

    gateway = SteamGateway.__new__(SteamGateway)

    gateway.settings = MagicMock()
    gateway.client = MagicMock()
    gateway.client.call = AsyncMock()

    return gateway


@pytest.mark.asyncio
async def test_resolve_vanity_url_success(
    steam_gateway: SteamGateway,
) -> None:
    """Успешное получение SteamID по vanity URL."""

    steam_gateway.client.call.return_value = {
        "response": {
            "steamid": "76561198000000000",
            "success": 1,
        }
    }

    result = await steam_gateway.resolve_vanity_url(
        vanity_url="sample_user"
    )

    assert result == "76561198000000000"

    steam_gateway.client.call.assert_awaited_once_with(
        interface="ISteamUser",
        method="ResolveVanityURL",
        vanityurl="sample_user",
    )


@pytest.mark.asyncio
async def test_resolve_vanity_url_not_found(
    steam_gateway: SteamGateway,
) -> None:
    """Обработка ситуации, когда vanity URL не найден."""

    steam_gateway.client.call.return_value = {
        "response": {
            "success": 42,
        }
    }

    with pytest.raises(SteamAPIError):
        await steam_gateway.resolve_vanity_url(
            vanity_url="unknown_user"
        )


@pytest.mark.asyncio
async def test_resolve_vanity_url_without_steam_id(
    steam_gateway: SteamGateway,
) -> None:
    """Обработка ответа без SteamID."""

    steam_gateway.client.call.return_value = {
        "response": {
            "success": 1,
        }
    }

    with pytest.raises(SteamAPIError):
        await steam_gateway.resolve_vanity_url(
            vanity_url="sample_user"
        )


@pytest.mark.asyncio
async def test_get_player_summary_success(
    steam_gateway: SteamGateway,
) -> None:
    """Успешное получение информации о профиле."""

    expected_player = {
        "steamid": "76561198000000000",
        "personaname": "Sample Player",
        "profileurl": "https://steamcommunity.com/profiles/76561198000000000",
    }

    steam_gateway.client.call.return_value = {
        "response": {
            "players": [expected_player],
        }
    }

    result = await steam_gateway.get_player_summary(
        steam_id="76561198000000000"
    )

    assert result == expected_player

    steam_gateway.client.call.assert_awaited_once_with(
        interface="ISteamUser",
        method="GetPlayerSummaries",
        version="v0002",
        steamids="76561198000000000",
    )


@pytest.mark.asyncio
async def test_get_player_summary_not_found(
    steam_gateway: SteamGateway,
) -> None:
    """Обработка отсутствующего профиля."""

    steam_gateway.client.call.return_value = {
        "response": {
            "players": [],
        }
    }

    with pytest.raises(SteamAPIError):
        await steam_gateway.get_player_summary(
            steam_id="76561198000000000"
        )


@pytest.mark.asyncio
async def test_get_owned_games_success(
    steam_gateway: SteamGateway,
) -> None:
    """Успешное получение библиотеки игр."""

    expected_games = [
        {
            "appid": 730,
            "name": "Counter-Strike 2",
            "playtime_forever": 1200,
        },
        {
            "appid": 570,
            "name": "Dota 2",
            "playtime_forever": 500,
        },
    ]

    steam_gateway.client.call.return_value = {
        "response": {
            "games": expected_games,
        }
    }

    games, available = await steam_gateway.get_owned_games(
        steam_id="76561198000000000"
    )

    assert games == expected_games
    assert available is True

    steam_gateway.client.call.assert_awaited_once_with(
        interface="IPlayerService",
        method="GetOwnedGames",
        steamid="76561198000000000",
        include_appinfo=1,
        include_played_free_games=1,
    )


@pytest.mark.asyncio
async def test_get_owned_games_empty(
    steam_gateway: SteamGateway,
) -> None:
    """Проверка доступной, но пустой библиотеки игр."""

    steam_gateway.client.call.return_value = {
        "response": {
            "games": [],
        }
    }

    games, available = await steam_gateway.get_owned_games(
        steam_id="76561198000000000"
    )

    assert games == []
    assert available is True


@pytest.mark.asyncio
async def test_get_owned_games_unavailable(
    steam_gateway: SteamGateway,
) -> None:
    """Проверка недоступной библиотеки игр."""

    steam_gateway.client.call.return_value = {
        "response": {}
    }

    games, available = await steam_gateway.get_owned_games(
        steam_id="76561198000000000"
    )

    assert games == []
    assert available is False


@pytest.mark.asyncio
async def test_get_recently_played_games_success(
    steam_gateway: SteamGateway,
) -> None:
    """Успешное получение недавно запущенных игр."""

    expected_games = [
        {
            "appid": 730,
            "name": "Counter-Strike 2",
            "playtime_2weeks": 300,
            "playtime_forever": 1200,
        }
    ]

    steam_gateway.client.call.return_value = {
        "response": {
            "games": expected_games,
        }
    }

    games, available = await steam_gateway.get_recently_played_games(
        steam_id="76561198000000000"
    )

    assert games == expected_games
    assert available is True

    steam_gateway.client.call.assert_awaited_once_with(
        interface="IPlayerService",
        method="GetRecentlyPlayedGames",
        steamid="76561198000000000",
        count=10,
    )


@pytest.mark.asyncio
async def test_get_recently_played_games_empty(
    steam_gateway: SteamGateway,
) -> None:
    """Проверка отсутствия недавно запущенных игр."""

    steam_gateway.client.call.return_value = {
        "response": {
            "games": [],
        }
    }

    games, available = await steam_gateway.get_recently_played_games(
        steam_id="76561198000000000"
    )

    assert games == []
    assert available is True


@pytest.mark.asyncio
async def test_get_recently_played_games_unavailable(
    steam_gateway: SteamGateway,
) -> None:
    """Проверка недоступности информации о последних играх."""

    steam_gateway.client.call.return_value = {
        "response": {}
    }

    games, available = await steam_gateway.get_recently_played_games(
        steam_id="76561198000000000"
    )

    assert games == []
    assert available is False


def test_parse_steam_id64() -> None:
    assert SteamProfileService.parse_steam_identifier(value="76561198000000000") == ("steam_id", "76561198000000000")


def test_parse_vanity_profile_url() -> None:
    assert SteamProfileService.parse_steam_identifier(value="https://steamcommunity.com/id/sample_user") == ("vanity", "sample_user")


def test_parse_profiles_url() -> None:
    assert SteamProfileService.parse_steam_identifier(value="steamcommunity.com/profiles/76561198000000000") == ("steam_id", "76561198000000000")


@pytest.mark.parametrize("value", [
    "Player123",
    "https://example.com/id/sample",
    "https://steamcommunity.com/id/",
    "https://steamcommunity.com/profiles/not-a-steam-id",
])
def test_reject_invalid_identifiers(value: str) -> None:
    with pytest.raises(SteamIdentifierError):
        SteamProfileService.parse_steam_identifier(value=value)


def test_normalize_profile_keeps_private_data_unavailable_distinct_from_empty() -> None:
    result = SteamProfileService.normalize_profile_info(
        player={"steamid": "76561198000000000", "personaname": "Player"},
        games=[],
        recent_games=[],
        games_available=False,
        recent_games_available=False,
    )
    assert result["steam_id"] == "76561198000000000"
    assert result["games"] == []
    assert result["games_available"] is False
    assert result["recent_games_available"] is False
