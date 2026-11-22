"""Очередь на проверку человеком и продвижение элементов в базу знаний на основе транзакционных данных"""
from __future__ import annotations

from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.db import KnowledgeBase, UncertainExample


LOW_SCORE_THRESHOLD = 0.65


class ActiveLearningHandler:
    """Класс активного обучения"""

    def __init__(self):
        pass


    @staticmethod
    async def enqueue_if_uncertain(
        session: AsyncSession,
        *,
        input_text: str,
        model_output: str,
        critic_score: float | None,
        validation_passed: bool = True,
        threshold: float = LOW_SCORE_THRESHOLD
    ) -> UncertainExample | None:
        """Очередь не прошла проверку или получила низкий числовой балл"""

        if validation_passed and (critic_score is None or critic_score >= threshold):
            return None

        example = UncertainExample(
            input_text=input_text,
            model_output=model_output,
            critic_score=critic_score,
            status="pending"
        )

        session.add(example)
        await session.commit()
        await session.refresh(example)

        return example


    @staticmethod
    async def pending_examples(
        session: AsyncSession,
        *,
        status: str = "pending",
        limit: int = 100
    ):
        """Получение примеров"""

        if status not in {"pending", "approved", "rejected"}:
            raise ValueError(
                "Invalid review status"
            )

        result = await session.scalars(
            select(UncertainExample).where(UncertainExample.status == status).order_by(UncertainExample.internal_id).limit(limit)
        )

        return list(result.all())


    @staticmethod
    async def review_example(
        session: AsyncSession,
        example_id: int,
        *,
        approve: bool,
        corrected_text: str | None = None
    ) -> tuple[Type[UncertainExample], KnowledgeBase | None]:
        """Проведение ревью по примеру решение"""

        example = await session.get(UncertainExample, example_id)

        if example is None:
            raise LookupError(
                "Review example not found"
            )

        if example.status != "pending":
            raise ValueError(
                "Example has already been reviewed"
            )

        text = (corrected_text or example.model_output).strip()
        if approve and not text:
            raise ValueError(
                "Approved output must not be empty"
            )

        kb = None
        if approve:
            kb = KnowledgeBase(
                source_text=example.input_text,
                target_text=text,
                category="hitl-approved"
            )
            session.add(kb)
            example.model_output = text

        example.status = "approved" if approve else "rejected"
        await session.commit()
        await session.refresh(example)

        if kb is not None:
            await session.refresh(kb)

        return example, kb
