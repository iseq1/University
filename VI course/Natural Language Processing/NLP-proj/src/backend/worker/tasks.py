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
