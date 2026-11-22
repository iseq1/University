"""Эндпоинты для ручной проверки с разграничением ролей и асинхронной переиндексации"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.api.deps import require_editor
from src.backend.db import User, UncertainExample, Session
from src.backend.hitl import ActiveLearningHandler, CacheHandler, save_feedback
from src.backend.api.schemas import FeedbackPayload, ReviewPayload
from src.backend.utils.utils import serialize_example


async_session = Session().get_session


class HitlRouter:
    """API-класс, описывающий endpoint-ы для ручной проверки с разграничением ролей и асинхронной переиндексации"""


    def __init__(self):
        self.router = APIRouter(prefix="/api/v1/hitl", tags=["hitl"], dependencies=[Depends(require_editor)])
        self._register_routes()


    def _register_routes(self) -> None:
        """Регистрация endpoint-ов hitl"""

        self.router.add_api_route(
            "/queue",
            endpoint=self.queue,
            methods=["GET"],
        )

        self.router.add_api_route(
            "/{example_id}/approve",
            endpoint=self.approve,
            methods=["POST"],
        )

        self.router.add_api_route(
            "/{example_id}/reject",
            endpoint=self.reject,
            methods=["POST"],
        )

        self.router.add_api_route(
            "/{example_id}/feedback",
            endpoint=self.feedback,
            methods=["POST"],
        )

        self.router.add_api_route(
            "/reindex",
            endpoint=self.reindex,
            methods=["POST"],
            status_code=status.HTTP_202_ACCEPTED
        )


    @staticmethod
    async def queue(
        status: str = "pending",
        limit: int = Query(100, ge=1, le=500),
        session: AsyncSession = Depends(async_session)
    ):
        """Получение очереди"""

        try:
            items = await ActiveLearningHandler.pending_examples(
                session,
                status=status,
                limit=limit
            )

        except ValueError as exc:
            raise HTTPException(
                422,
                detail=str(exc)
            ) from exc

        return {
            "items": [serialize_example(x) for x in items],
            "count": len(items)
        }


    @staticmethod
    async def _decide(example_id: int, session: AsyncSession, approve: bool, corrected_text: str | None):
        """Принятие решения"""

        try:
            example, kb = await ActiveLearningHandler.review_example(
                session,
                example_id,
                approve=approve,
                corrected_text=corrected_text
            )

        except LookupError as exc:
            raise HTTPException(
                404,
                detail=str(exc)
            ) from exc

        except ValueError as exc:
            raise HTTPException(
                409,
                detail=str(exc)
            ) from exc

        scheduled = False
        if kb is not None:
            try:
                from src.backend.worker.tasks import reindex_knowledge_base_task
                reindex_knowledge_base_task.delay()
                scheduled = True

            except Exception:
                scheduled = False

        return {
            "example": serialize_example(example),
            "knowledge_base_internal_id": kb.internal_id if kb else None,
            "reindex_required": bool(kb),
            "reindex_scheduled": scheduled
        }


    async def approve(
        self,
        example_id: int,
        payload: ReviewPayload,
        session: AsyncSession = Depends(async_session)
    ):
        """Фиксация одобрения"""

        return await self._decide(
            example_id=example_id,
            session=session,
            approve=True,
            corrected_text=payload.corrected_text
        )


    async def reject(
        self,
        example_id: int,
        session: AsyncSession = Depends(async_session)
    ):
        """Фиксация отказа"""
        return await self._decide(
            example_id=example_id,
            session=session,
            approve=False,
            corrected_text=None
        )


    async def feedback(
        self,
        example_id: int,
        payload: FeedbackPayload,
        session: AsyncSession = Depends(async_session)
    ):
        """Фиксация ОС"""
        return await self._decide(
            example_id=example_id,
            session=session,
            approve=True,
            corrected_text=payload.corrected_text
        )


    @staticmethod
    async def reindex():
        """Переиндексация"""
        from src.backend.worker import reindex_knowledge_base_task
        task = reindex_knowledge_base_task.delay()
        return {
            "task_id": task.id,
            "status": "queued"
        }
