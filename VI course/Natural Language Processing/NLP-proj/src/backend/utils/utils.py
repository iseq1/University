"""Общие утилиты"""
import hashlib
import uuid


def custom_hash(value: str | None) -> str | None:
    """Получение хэш-значения строки"""
    return hashlib.sha256(value.encode("utf-8")).hexdigest() if value is not None else None


def make_uuid() -> str:
    """Формирование uuid-строки"""
    return str(uuid.uuid4())
