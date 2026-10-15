"""Константы уровня приложения"""
from enum import Enum

APP_NAME = "Gamer Passport"
API_PREFIX = "/api"
HEALTHCHECK_PATH = "/healthz"

DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FILE = "logs/app.log"


class UserRole(Enum):
    """Класс, описывающий возможные роли пользователя"""

    USER = "user"
    EDITOR = "editor"
    ADMIN = "admin"


class AuthDetails(Enum):
    """Класс, описывающий детали аутентификации"""

    _401_ERROR = "Неверные или отсутствующие учетные данные для аутентификации."
    _401_NONE = "Пользователь неактивен или не существует."
    _403_INACTIVE = "Учетная запись деактивирована."
    _403_ADMIN = "Отсутствуют права доступа. Требуются права администратора!"
    _403_EDITOR = "Отсутствуют права доступа. Требуются права редактора!"
    _409_EXISTING = "Электронная почта или имя пользователя уже зарегистрированы."


LLM_PROVIDERS = (
    "ollama",
    "huggingface",
    "openai",
    "anthropic",
    "google",
    "openrouter",
)
