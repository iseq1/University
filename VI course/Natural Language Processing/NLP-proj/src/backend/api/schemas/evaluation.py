"""Pydantic-схемы необходимые для получения оценки"""

from pydantic import BaseModel, Field, model_validator


class EvaluateRequest(BaseModel):
    reference: str = Field(min_length=1)
    prediction: str = Field(min_length=1)
    model_name: str = "configured-llm"
    mode: str = "full"
    include_bertscore: bool = False


class EvaluationBatchRequest(BaseModel):
    models: list[str] = Field(min_length=1, max_length=2)
    modes: list[str] = Field(default_factory=lambda: ["baseline", "+dict", "+rag", "+agents", "+ensemble"])
    sample_size: int = Field(default=20, ge=20, le=100)
    seed: int = 42

    @model_validator(mode="after")
    def validate_evaluation_options(self) -> "EvaluationBatchRequest":
        """Валидация запроса оценки"""
        from src.backend.evaluation import SUPPORTED_MODES, SUPPORTED_PROVIDERS

        if self.sample_size not in (20, 50, 100):
            raise ValueError(
                "sample_size must be 20, 50 or 100"
            )

        if not self.modes or set(self.modes) - set(SUPPORTED_MODES):
            raise ValueError(
                f"modes must be selected from {SUPPORTED_MODES}"
            )

        if set(self.models) - set(SUPPORTED_PROVIDERS):
            raise ValueError(
                f"models must be selected from {SUPPORTED_PROVIDERS}"
            )

        return self
