"""Схемы Pydantic для эндпоинтов ручной проверки с разграничением ролей и асинхронной переиндексации"""

from pydantic import BaseModel, Field


class ReviewPayload(BaseModel):
    """Тело ревью"""
    corrected_text: str | None = Field(default=None, max_length=20000)


class FeedbackPayload(BaseModel):
    """Тело ОС"""
    corrected_text: str = Field(min_length=1, max_length=20000)
