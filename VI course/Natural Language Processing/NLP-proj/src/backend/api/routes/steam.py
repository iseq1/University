"""API-роуты импорта и получения данных профилей Steam"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.core import get_settings, SteamIdentifierError, SteamAPIError
from src.backend.db import User, Session
from src.backend.service import SteamProfileService
from src.backend.api.schemas import SteamProfileResponse, SteamProfileRequest
from src.backend.api.deps import get_current_user


class SteamRouter:
    """API-класс, описывающий endpoint-ы импорта и получения данных профилей Steam"""


    def __init__(self):
        self.router = APIRouter(prefix="/api/v1/steam", tags=["steam"])
        self.settings = get_settings()
        self._register_routes()


    def _register_routes(self) -> None:
        """Регистрация endpoint-ов авторизации"""

        self.router.add_api_route(
            "/profile",
            endpoint=self.import_steam_profile,
            methods=["POST"],
            response_model=SteamProfileResponse,
            status_code=status.HTTP_200_OK,
        )


    async def import_steam_profile(
        self,
        data: SteamProfileRequest,
        _: User = Depends(get_current_user),
        session: AsyncSession = Depends(Session().get_session),
    ) -> SteamProfileResponse:
        """Импорт данных Steam-профиля"""

        if not self.settings.steam_api_key or not self.settings.steam_api_key.get_secret_value().strip():
            raise HTTPException(
                status_code=503,
                detail="Ключ Steam Web API не настроен"
            )

        try:
            profile, cached = await SteamProfileService(session).get_steam_profile_info(
                identifier=data.profile_url,
                refresh=data.refresh
            )

        except SteamIdentifierError as exc:
            raise HTTPException(
                status_code=422,
                detail=str(exc)
            ) from exc

        except SteamAPIError as exc:
            raise HTTPException(
                status_code=502,
                detail=str(exc)
            ) from exc

        return SteamProfileResponse(
            steam_id=str(profile["steam_id"]),
            profile=profile,
            cached=cached
        )