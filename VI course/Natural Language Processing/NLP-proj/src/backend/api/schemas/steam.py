"""Pydantic-схемы необходимые для взаимодействия со Steam"""

from typing import Any

from pydantic import BaseModel, Field


class SteamProfileRequest(BaseModel):
    """Схема запроса для получения инфо о Steam-профиле"""
    profile_url: str = Field(min_length=3, max_length=500)
    refresh: bool = False


class SteamProfileResponse(BaseModel):
    """Схема ответа с инфо о Steam-профиле"""
    steam_id: str
    profile: dict[str, Any]
    cached: bool