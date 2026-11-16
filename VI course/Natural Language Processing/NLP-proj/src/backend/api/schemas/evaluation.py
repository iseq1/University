"""Pydantic-схемы необходимые для получения оценки"""

from pydantic import BaseModel, Field


class EvaluateRequest(BaseModel):
    reference: str = Field(min_length=1)
    prediction: str = Field(min_length=1)
    model_name: str = "configured-llm"
    mode: str = "full"
    include_bertscore: bool = False
