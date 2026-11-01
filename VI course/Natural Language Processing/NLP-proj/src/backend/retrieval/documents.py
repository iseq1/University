"""Представление документов, используемых в RAG"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RetrievedDocument:
    """Пример записи базы знаний"""

    id: str
    source_text: str
    target_text: str
    category: str | None = None
