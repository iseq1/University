"""Фоновые задачи, выполняемые воркерами Celery."""
from __future__ import annotations

import asyncio
from typing import Any

from src.backend.db import Session
from src.backend.evaluation import EvaluationRunner
from src.backend.worker.celery_app import celery_app


async def _run_evaluation(**kwargs: Any) -> dict[str, Any]:
    """Выполнение оценки"""
    result = None

    session_generator = Session().get_session()
    session = await anext(session_generator)

    try:
        runner = EvaluationRunner(
            session,
            include_bertscore=bool(kwargs.pop("include_bertscore", False)),
        )
        result = await runner.evaluate(**kwargs)

    finally:
        await session_generator.aclose()
        return result


@celery_app.task(name="evaluate_model_task")
def evaluate_model_task(
    model: str,
    mode: str,
    sample_size: int,
    dataset_path: str = "data/generated/knowledge_base_test.json",
    seed: int = 42,
) -> dict[str, Any]:
    """Выполнить оценку одной комбинации «поставщик/способ» в фоновом режиме"""
    return asyncio.run(_run_evaluation(
        providers=[model],
        modes=[mode],
        sample_size=sample_size,
        dataset_path=dataset_path,
        seed=seed,
    ))


@celery_app.task(name="compare_models_task")
def compare_models_task(
    models: list[str],
    modes: list[str],
    sample_size: int,
    dataset_path: str = "data/generated/knowledge_base_test.json",
    seed: int = 42,
) -> dict[str, Any]:
    """Сравнить запрошенные провайдеры и режимы в фоновом режиме."""
    return asyncio.run(_run_evaluation(
        providers=models,
        modes=modes,
        sample_size=sample_size,
        dataset_path=dataset_path,
        seed=seed,
    ))

@celery_app.task(name="reindex_knowledge_base_task")
def reindex_knowledge_base_task(batch_size: int = 64) -> dict[str, int]:
    """Обновить Qdrant на основе утвержденных примеров знаний из SQL"""
    from src.scripts.index_knowledge_base import IndexKnowledgeBase
    return {
        "indexed": asyncio.run(IndexKnowledgeBase().run_index(batch_size))
    }


@celery_app.task(name="cleanup_cache_task")
def cleanup_cache_task(ttl_hours: int = 24) -> dict[str, int]:
    """Удалить старые строки из кэша генераций LLM"""
    from src.backend.hitl import CacheHandler

    async def execute():
        """Выполнить отчистку кэша"""
        result = None
        session_generator = Session().get_session()
        session = await anext(session_generator)

        try:
            result = await CacheHandler.clear_expired(session, ttl_hours=ttl_hours)

        finally:
            await session_generator.aclose()
            return result


    return {
        "deleted": asyncio.run(execute())
    }


@celery_app.task(name="generate_batch_task")
def generate_batch_task(items: list[dict]) -> dict[str, Any]:
    """Создание пакета с помощью существующего конвейера API"""
    from src.backend.api.routes.generation import _generate
    from src.backend.api.schemas.generation import GenerateRequest

    async def execute(items: list):
        """Выполнение генерации"""

        results = []
        session_generator = Session().get_session()
        session = await anext(session_generator)

        try:
            for item in items:

                try:
                    results.append((await _generate(GenerateRequest.model_validate(item), session)).model_dump(mode="json"))

                except Exception as exc:
                    results.append({
                        "error": type(exc).__name__
                    })

        finally:
            await session_generator.aclose()
            return {
                "count": len(results),
                "results": results
            }

    return asyncio.run(execute(items=items))

