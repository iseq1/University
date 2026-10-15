"""API-роуты аутентификации"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.api.deps import get_current_user
from src.backend.api.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from src.backend.db.models import User
from src.backend.db.session import Session
from src.backend.utils.security import Security
from src.backend.core import AuthDetails


class AuthRouter:
    """API-класс, описывающий endpoint-ы аутентификации"""


    def __init__(self):
        self.router = APIRouter(prefix="/auth", tags=["auth"])
        self.security = Security()
        self._register_routes()


    def _register_routes(self) -> None:
        """Регистрация endpoint-ов авторизации"""

        self.router.add_api_route(
            "/register",
            endpoint=self.register,
            methods=["POST"],
            response_model=UserResponse,
            status_code=status.HTTP_201_CREATED,
        )

        self.router.add_api_route(
            "/login",
            endpoint=self.login,
            methods=["POST"],
            response_model=TokenResponse,
        )

        self.router.add_api_route(
            "/me",
            endpoint=self.me,
            methods=["GET"],
            response_model=UserResponse,
        )


    async def register(
        self,
        data: RegisterRequest,
        session: AsyncSession = Depends(Session().get_session),
    ) -> User:
        """Регистрация нового пользователя с ролью по умолчанию"""

        # Проверка существования пользователя
        existing = await session.execute(
            select(User).where(
                or_(
                    User.email == data.email,
                    User.username == data.username,
                )
            )
        )

        # Если такой пользователь уже есть > возвращаем ошибку
        if existing.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=AuthDetails._409_EXISTING.value,
            )

        # Создание записи о новом пользователе
        user = User(
            email=data.email,
            username=data.username,
            hashed_password=self.security.hash_password(data.password),
        )
        session.add(user)

        try:
            await session.commit()
            await session.refresh(user)
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=AuthDetails._409_EXISTING.value,
            ) from None

        return user


    async def login(
        self,
        data: LoginRequest,
        session: AsyncSession = Depends(Session().get_session),
    ) -> TokenResponse:
        """Аутентификация пользователя"""

        # Поиск зарегистрированного пользователя
        result = await session.execute(
            select(User).where(User.email == data.email)
        )
        user = result.scalar_one_or_none()

        # Если пользователя нет > отдаем ошибку
        if user is None or not self.security.verify_password(
            data.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=AuthDetails._401_ERROR.value,
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Если запись не активна > отдаем ошибку
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=AuthDetails._403_INACTIVE.value,
            )

        return TokenResponse(
            access_token=self.security.create_access_token(
                str(user.source_id),
                user.role,
            )
        )


    @staticmethod
    async def me(current_user: User = Depends(get_current_user),) -> User:
        """Получение актуального пользователя"""
        return current_user