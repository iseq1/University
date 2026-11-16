"""Схемы Pydantic для эндпоинтов генерации"""
from typing import Any

from pydantic import BaseModel, Field, model_validator


class GenerateRequest(BaseModel):
    steam_id: str | None = Field(default=None, min_length=1, max_length=100)
    profile_url: str | None = Field(default=None, max_length=500)
    profile: dict[str, Any] = Field(default_factory=dict)
    input_text: str | None = Field(default=None, max_length=30000)
    mode: str = Field(default="full", pattern="^(baseline|full)$")
    use_cache: bool = True

    @model_validator(mode="after")
    def validate_profile_identifier(self) -> "GenerateRequest":
        """Валидация идентификатора запроса"""

        if not self.steam_id and not self.profile_url:
            raise ValueError(
                "Укажите steam_id или profile_url"
            )

        return self


class RetrievedSource(BaseModel):
    document_id: str
    source_text: str
    target_text: str
    category: str | None = None
    score: float


class GenerateResponse(BaseModel):
    request_id: str
    steam_id: str
    summary: str
    mode: str
    cached: bool = False
    validation_passed: bool = True
    critic_score: float | None = None
    warnings: list[str] = Field(default_factory=list)
    retrieved_sources: list[RetrievedSource] = Field(default_factory=list)


class BatchGenerateRequest(BaseModel):
    items: list[GenerateRequest] = Field(min_length=1, max_length=20)
