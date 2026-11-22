"""Общие утилиты"""
from typing import Type
import hashlib
import uuid

from src.backend.db import UncertainExample


def custom_hash(value: str | None) -> str | None:
    """Получение хэш-значения строки"""
    return hashlib.sha256(value.encode("utf-8")).hexdigest() if value is not None else None


def make_uuid() -> str:
    """Формирование uuid-строки"""
    return str(uuid.uuid4())


def serialize_example(example: UncertainExample | Type[UncertainExample]):
    """Сериализация модели UncertainExample"""
    return {
        "internal_id": example.internal_id,
        "input_text": example.input_text,
        "model_output": example.model_output,
        "critic_score": example.critic_score,
        "status": example.status
    }
