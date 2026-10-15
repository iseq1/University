"""Утилиты безопасности"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from src.backend.core import get_settings


class Security:
    """Класс, описывающий методы защиты информации"""

    def __init__(self):
        self.settings = get_settings()

    @staticmethod
    def hash_password(password: str) -> str:
        """Хеширование пароля"""
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")


    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Верификация пароля"""
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))



    def create_access_token(self, subject: str, role: str) -> str:
        """Создание JWT-токена доступа"""
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=self.settings.access_token_expire_minutes)
        payload = {
            "sub": subject,
            "role": role,
            "exp": expires_at,
        }
        return jwt.encode(
            payload,
            self.settings.jwt_secret_key.get_secret_value(),
            algorithm=self.settings.jwt_algorithm
        )


    def decode_access_token(self, token: str) -> dict:
        """Проверка JWT-токена доступа"""
        return jwt.decode(
            token,
            self.settings.jwt_secret_key.get_secret_value(),
            algorithms=[self.settings.jwt_algorithm],
        )
