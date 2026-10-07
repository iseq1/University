"""SQLAlchemy-модели для взаимодействия с БД"""

from datetime import datetime, date

from sqlalchemy import JSON, Boolean, Date, DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс БД-модели"""


class User(Base):
    """Модель пользователя"""

    __tablename__ = "users"

    npart_year_month: Mapped[date] =  mapped_column(Date, server_default=func.now(), nullable=False)
    load_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False) # Аналог created_at
    update_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False)
    source_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="user")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class KnowledgeBase(Base):
    """Модель базы знаний"""

    __tablename__ = "knowledge_base"

    npart_year_month: Mapped[date] =  mapped_column(Date, server_default=func.now(), nullable=False)
    load_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False) # Аналог created_at
    update_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False)
    internal_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_text: Mapped[str] = mapped_column(Text, nullable=False)
    target_text: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)


class Glossary(Base):
    """Модель глоссария"""

    __tablename__ = "glossary"

    npart_year_month: Mapped[date] =  mapped_column(Date, server_default=func.now(), nullable=False)
    load_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False) # Аналог created_at
    update_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False)
    internal_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    term: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    definition: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)


class UncertainExample(Base):
    """Модель проверенных примеров"""

    __tablename__ = "uncertain_examples"

    npart_year_month: Mapped[date] =  mapped_column(Date, server_default=func.now(), nullable=False)
    load_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False) # Аналог created_at
    update_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False)
    internal_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    input_text: Mapped[str] = mapped_column(Text, nullable=False)
    model_output: Mapped[str] = mapped_column(Text, nullable=False)
    critic_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True)


class Cache(Base):
    """Модель кэша"""

    __tablename__ = "cache"

    npart_year_month: Mapped[date] =  mapped_column(Date, server_default=func.now(), nullable=False)
    load_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False) # Аналог created_at
    update_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False)
    internal_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    input_key: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    output: Mapped[str] = mapped_column(Text, nullable=False)
    hits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class EvaluationResult(Base):
    """Модель результатов"""

    __tablename__ = "evaluation_results"

    npart_year_month: Mapped[date] =  mapped_column(Date, server_default=func.now(), nullable=False)
    load_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False) # Аналог created_at
    update_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False)
    internal_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    model_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    mode: Mapped[str] = mapped_column(String(100), nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False)
    metrics_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    evaluation_time: Mapped[float | None] = mapped_column(Float, nullable=True)


class ModelComparison(Base):
    """Модель сравнения"""

    __tablename__ = "model_comparisons"

    npart_year_month: Mapped[date] =  mapped_column(Date, server_default=func.now(), nullable=False)
    load_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False) # Аналог created_at
    update_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False)
    internal_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    models_compared: Mapped[list] = mapped_column(JSON, nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False)
    results_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    winner: Mapped[str | None] = mapped_column(String(255), nullable=True)


class ReasoningLog(Base):
    """Модель логов размышлений"""

    __tablename__ = "reasoning_logs"

    npart_year_month: Mapped[date] =  mapped_column(Date, server_default=func.now(), nullable=False)
    load_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False) # Аналог created_at
    update_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False)
    internal_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    agent_name: Mapped[str] = mapped_column(String(100), nullable=False)
    input_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    output_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    model_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    parameters: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)


class LLMCall(Base):
    """Модель трассировки вызовов LLM"""

    __tablename__ = "llm_calls"

    npart_year_month: Mapped[date] =  mapped_column(Date, server_default=func.now(), nullable=False)
    load_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False) # Аналог created_at
    update_date: Mapped[datetime] = mapped_column(Date, server_default=func.now(), nullable=False)
    internal_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    agent_name: Mapped[str] = mapped_column(String(100), nullable=False)
    model_name: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    prompt_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    response_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    tokens_used: Mapped[int | None] = mapped_column(Integer, nullable=True)
    latency_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
