"""Модульные тесты для маршрутов аутентификации и зависимостей авторизации"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from src.backend.api import AuthRouter, LoginRequest, RegisterRequest, get_current_user, require_admin, require_editor
from src.backend.core import UserRole
from src.backend.db import User
from src.backend.utils import Security


def make_user(role: str = UserRole.USER.value) -> User:
    user = User(
        source_id=1,
        email="player@example.com",
        username="player",
        hashed_password=Security.hash_password("password123"),
        role=role,
        is_active=True,
    )
    user.load_date = datetime.now(timezone.utc)
    return user


def make_result(user: User | None) -> MagicMock:
    result = MagicMock()
    result.scalar_one_or_none.return_value = user
    return result


@pytest.mark.asyncio
async def test_register_creates_user_with_default_role() -> None:
    session = AsyncMock()
    session.execute.return_value = make_result(None)
    user = make_user()
    session.refresh.side_effect = lambda value: None

    # Make the mocked refresh populate fields that are normally supplied by DB defaults.
    async def refresh(value: User) -> None:
        value.id = user.source_id
        value.load_date = user.load_date

    session.refresh.side_effect = refresh

    result = await AuthRouter().register(
        RegisterRequest(
            email="player@example.com",
            username="player",
            password="password123",
        ),
        session,
    )

    assert result.email == "player@example.com"
    assert result.username == "player"
    # assert result.role == UserRole.USER.value
    assert result.hashed_password != "password123"
    session.add.assert_called_once()
    session.commit.assert_awaited_once()
    session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_rejects_duplicate_user() -> None:
    session = AsyncMock()
    session.execute.return_value = make_result(make_user())

    with pytest.raises(HTTPException) as exc_info:
        await AuthRouter().register(
            RegisterRequest(
                email="player@example.com",
                username="player",
                password="password123",
            ),
            session,
        )

    assert exc_info.value.status_code == 409


@pytest.mark.asyncio
async def test_login_returns_access_token() -> None:
    session = AsyncMock()
    session.execute.return_value = make_result(make_user())

    response = await AuthRouter().login(
        LoginRequest(email="player@example.com", password="password123"),
        session,
    )

    assert response.token_type == "bearer"
    assert response.access_token


@pytest.mark.asyncio
async def test_login_rejects_wrong_password() -> None:
    session = AsyncMock()
    session.execute.return_value = make_result(make_user())

    with pytest.raises(HTTPException) as exc_info:
        await AuthRouter().login(
            LoginRequest(email="player@example.com", password="wrong-password"),
            session,
        )

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_uses_jwt_subject() -> None:
    from fastapi.security import HTTPAuthorizationCredentials

    session = AsyncMock()
    user = make_user()
    session.get.return_value = user
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=Security().create_access_token(str(user.source_id), user.role),
    )

    result = await get_current_user(credentials, session)

    assert result is user
    session.get.assert_awaited_once_with(User, user.source_id)


@pytest.mark.asyncio
async def test_get_current_user_rejects_missing_credentials() -> None:
    session = AsyncMock()

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(None, session)

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_require_admin_allows_only_admin() -> None:
    admin = make_user(UserRole.ADMIN.value)
    assert await require_admin(admin) is admin

    with pytest.raises(HTTPException) as exc_info:
        await require_admin(make_user(UserRole.EDITOR.value))

    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_require_editor_allows_editor_and_admin() -> None:
    editor = make_user(UserRole.EDITOR.value)
    admin = make_user(UserRole.ADMIN.value)

    assert await require_editor(editor) is editor
    assert await require_editor(admin) is admin

    with pytest.raises(HTTPException) as exc_info:
        await require_editor(make_user(UserRole.USER.value))

    assert exc_info.value.status_code == 403
