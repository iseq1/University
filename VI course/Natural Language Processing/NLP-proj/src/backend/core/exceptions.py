"""Классы исключений в рамках приложения"""


class GamerPassportError(Exception):
    """Базовое исключение для ошибок уровня приложения"""


class ConfigurationError(GamerPassportError):
    """Возникает, если конфигурация приложения недопустима"""


class ExternalServiceError(GamerPassportError):
    """Возникает, когда внешний сервис недоступен или не может быть использован"""
