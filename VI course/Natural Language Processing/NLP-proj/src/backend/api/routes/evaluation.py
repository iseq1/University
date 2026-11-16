"""Эндпоинты для оценки качества текста и отслеживания запросов"""

from __future__ import annotations

import time
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.db import Session, EvaluationResult, LLMCall, ReasoningLog, User
from src.backend.evaluation import calculate_metrics
from src.backend.api.schemas.evaluation import EvaluateRequest
from src.backend.api.deps import get_current_user


async_session = Session().get_session


class EvaluationRouter:
    """API-класс, описывающий endpoint-ы для оценки качества текста и отслеживания запросов"""


    def __init__(self):
        self.router = APIRouter(prefix="/api/v1", tags=["evaluation"])
        self._register_routes()


    def _register_routes(self) -> None:
        """Регистрация endpoint-ов авторизации"""

        self.router.add_api_route(
            "/evaluate",
            endpoint=self.evaluate,
            methods=["POST"],
        )

        self.router.add_api_route(
            "/evaluate/history",
            endpoint=self.get_evaluation_history,
            methods=["GET"],
        )

        self.router.add_api_route(
            "/evaluations",
            endpoint=self.get_evaluation_history,
            methods=["GET"],
        )

        self.router.add_api_route(
            "/requests/{request_id}/reasoning_log",
            endpoint=self.get_reasoning_log,
            methods=["GET"],
        )

        self.router.add_api_route(
            "/history/{request_id}",
            endpoint=self.get_reasoning_log,
            methods=["GET"],
        )


    @staticmethod
    async def evaluate(
        data: EvaluateRequest,
        _: User = Depends(get_current_user),
        session: AsyncSession = Depends(async_session),
    ):
        """Получение оценки"""

        started = time.perf_counter()

        try:
            metrics = calculate_metrics(
                reference=data.reference,
                prediction=data.prediction,
                include_bertscore=data.include_bertscore
            )

        except (ValueError, RuntimeError) as exc:
            raise HTTPException(
                status_code=422,
                detail=str(exc)
            ) from exc

        finally:
            elapsed = time.perf_counter() - started

        record = EvaluationResult(
            model_name=data.model_name,
            mode=data.mode,
            sample_size=1,
            metrics_json=metrics,
            evaluation_time=elapsed,
        )

        session.add(record)

        await session.commit(); await session.refresh(record)

        return {
            "internal_id": record.internal_id,
            "model_name": record.model_name,
            "mode": record.mode,
            "sample_size": 1,
            "metrics": metrics,
            "evaluation_time": elapsed
        }


    @staticmethod
    async def get_evaluation_history(
        limit: int = 50,
        _: User = Depends(get_current_user),
        session: AsyncSession = Depends(async_session),
    ) -> list[dict[str, Any]]:
        """Получение истории оценок"""

        rows = (await session.execute(
            select(EvaluationResult).order_by(desc(EvaluationResult.npart_year_month)).limit(min(max(limit, 1), 200))
        )).scalars().all()

        return [
            {
                "internal_id": row.internal_id,
                "model_name": row.model_name,
                "mode": row.mode,
                "sample_size": row.sample_size,
                "metrics": row.metrics_json,
                "evaluation_time": row.evaluation_time,
                "npart_year_month": row.npart_year_month
            }
            for row in rows
        ]


    @staticmethod
    async def get_reasoning_log(
        request_id: str,
        _: User = Depends(get_current_user),
        session: AsyncSession = Depends(async_session),
    ) -> dict[str, Any]:
        """Получение reasoning-лога"""

        logs = (await session.execute(
            select(ReasoningLog).where(ReasoningLog.request_id == request_id).order_by(ReasoningLog.internal_id)
        )).scalars().all()

        calls = (await session.execute(
            select(LLMCall).where(LLMCall.request_id == request_id).order_by(LLMCall.internal_id)
        )).scalars().all()

        if not logs and not calls:
            raise HTTPException(
                status_code=404,
                detail="Request trace not found"
            )

        return {
            "request_id": request_id,
            "reasoning_log": [
                {
                    "agent": row.agent_name,
                    "input": row.input_summary,
                    "output": row.output_summary,
                    "model": row.model_name,
                    "parameters": row.parameters,
                    "status": row.status,
                    "started_at": row.started_at,
                    "finished_at": row.finished_at,
                }
                for row in logs
            ],
            "llm_calls": [
                {
                    "agent": row.agent_name,
                    "model": row.model_name,
                    "provider": row.provider,
                    "prompt_hash": row.prompt_hash,
                    "response_hash": row.response_hash,
                    "tokens_used": row.tokens_used,
                    "latency_ms": row.latency_ms,
                    "status": row.status,
                    "created_at": row.load_date,
                }
                for row in calls
            ],
        }
