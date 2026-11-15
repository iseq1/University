"""Классы исключений в рамках приложения"""


class GamerPassportError(Exception):
    """Базовое исключение для ошибок уровня приложения"""


class ConfigurationError(GamerPassportError):
    """Возникает, если конфигурация приложения недопустима"""


class ExternalServiceError(GamerPassportError):
    """Возникает, когда внешний сервис недоступен или не может быть использован"""


class SteamAPIError(RuntimeError):
    """Steam API вернул ошибку или непригодный для использования ответ"""


class SteamIdentifierError(ValueError):
    """Возникает, если предоставленный идентификатор профиля Steam является недействительным."""