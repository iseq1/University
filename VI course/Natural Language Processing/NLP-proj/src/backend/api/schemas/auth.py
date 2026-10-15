"""Pydantic-схемы необходимые для авторизации"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RegisterRequest(BaseModel):
    """Необходимая информация для регистрации нового пользователя"""

    email: str = Field(min_length=3, max_length=255)
    username: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    """Необходимые данные для авторизации"""

    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    """JWT-токен доступа"""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Публичное представление пользователя"""

    model_config = ConfigDict(from_attributes=True)

    source_id: int
    email: str
    username: str
    role: str
    is_active: bool
    load_date: datetime
