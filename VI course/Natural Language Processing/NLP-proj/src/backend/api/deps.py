"""Зависимости FastAPI для аутентификации и авторизации"""
from typing import Any, Type, Coroutine

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.api.schemas import UserResponse
from src.backend.core import UserRole, AuthDetails
from src.backend.db import User, Session
from src.backend.utils import Security


bearer_scheme = HTTPBearer(auto_error=False)


def _unauthorized(detail: str = None) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail or AuthDetails._401_ERROR.value,
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: AsyncSession = Depends(Session().get_session),
) -> Type[User]:
    """Возвращает активного аутентифицированного пользователя"""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise _unauthorized()

    try:
        security = Security()
        payload = security.decode_access_token(credentials.credentials)
        subject = payload.get("sub")
        user_id = int(subject) if subject is not None else None
    except (InvalidTokenError, TypeError, ValueError):
        raise _unauthorized() from None

    if user_id is None:
        raise _unauthorized()

    user = await session.get(User, user_id)
    if user is None or not user.is_active:
        raise _unauthorized(AuthDetails._401_NONE.value)

    return user


async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Проверка пользователя на принадлежность к авторизованному администратору."""
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=AuthDetails._403_ADMIN.value)
    return current_user


async def require_editor(current_user: User = Depends(get_current_user)) -> User:
    """Проверка пользователя на принадлежность к авторизованному редактору или администратору"""
    if current_user.role not in (UserRole.ADMIN.value, UserRole.EDITOR.value):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=AuthDetails._403_EDITOR.value)
    return current_user
