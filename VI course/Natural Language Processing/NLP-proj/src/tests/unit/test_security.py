"""Unit tests for password hashing and JWT security."""

from datetime import datetime, timezone

import jwt

from src.backend.core import get_settings
from src.backend.utils import Security


def test_password_hash_is_not_plaintext() -> None:
    password = "strong-password-123"
    password_hash = Security.hash_password(password)

    assert password_hash != password
    assert password_hash.startswith("$2")
    assert Security.verify_password(password, password_hash)
    assert not Security.verify_password("wrong-password", password_hash)


def test_create_and_decode_access_token() -> None:
    security = Security()
    token = security.create_access_token(subject="42", role="editor")
    payload = security.decode_access_token(token)

    assert payload["sub"] == "42"
    assert payload["role"] == "editor"
    assert "exp" in payload
    assert datetime.fromtimestamp(payload["exp"], tz=timezone.utc) > datetime.now(timezone.utc)


def test_invalid_token_is_rejected() -> None:
    settings = get_settings()
    security = Security()

    try:
        security.decode_access_token(
            jwt.encode(
                {"sub": "42"},
                "wrong-secret",
                algorithm=settings.jwt_algorithm,
            )
        )
    except jwt.InvalidTokenError:
        pass
    else:
        raise AssertionError("Invalid token must be rejected")
