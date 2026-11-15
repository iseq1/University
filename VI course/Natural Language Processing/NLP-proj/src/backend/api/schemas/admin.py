"""Pydantic-схемы необходимые для взаимодействия административного взаимодействия"""

from pydantic import BaseModel, Field


class KnowledgeItem(BaseModel):
    """Объект из базы знаний"""
    source_text: str = Field(min_length=1)
    target_text: str = Field(min_length=1)
    category: str | None = None


class GlossaryItem(BaseModel):
    """Объект из глоссария"""
    term: str = Field(min_length=1, max_length=500)
    definition: str = Field(min_length=1)
    category: str | None = None


class KnowledgeImport(BaseModel):
    """Импорт базы знаний"""
    items: list[KnowledgeItem] = Field(min_length=1, max_length=1000)


class CSVImport(BaseModel):
    """Импорт CSV"""
    csv_text: str = Field(min_length=1, max_length=2_000_000)
