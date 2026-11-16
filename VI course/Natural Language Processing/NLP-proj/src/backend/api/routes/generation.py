"""API-эндпоинты для генерации"""
from __future__ import annotations

import hashlib
import json
import logging
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.api.deps import get_current_user
from src.backend.core import get_settings
from src.backend.db import Session, Cache, ModelComparison, User
from src.backend.gateways.llm import LLMGateway, get_llm_gateway
from src.backend.retrieval.service import RetrivalService
from src.backend.core import SteamIdentifierError, SteamAPIError
from src.backend.service import SteamProfileService
from src.backend.agents import (
    CriticAgent,
    EditorAgent,
    ValidatorAgent,
    Supervisor,
)
from src.backend.api.schemas.generation import (
    BatchGenerateRequest,
    GenerateRequest,
    GenerateResponse,
    RetrievedSource,
)


logger = logging.getLogger(__name__)
async_session = Session().get_session


class GenerationRouter:
    """API-класс, описывающий endpoint-ы для генерации"""

    def __init__(self):
        self.router = APIRouter(prefix="/api/v1", tags=["generation"])
        self._register_routes()


    def _register_routes(self) -> None:
        """Регистрация endpoint-ов авторизации"""

        self.router.add_api_route(
            "/generate",
            endpoint=self.generate,
            methods=["POST"],
            response_model=GenerateResponse,
        )

        self.router.add_api_route(
            "/generate/batch",
            endpoint=self.generate_batch,
            methods=["POST"],
            response_model=BatchGenerateRequest,
        )

        self.router.add_api_route(
            "/generate/variants",
            endpoint=self.generate_variants,
            methods=["POST"],
            response_model=GenerateRequest,
        )

        self.router.add_api_route(
            "/generate/ensemble",
            endpoint=self.generate_ensemble,
            methods=["POST"],
            response_model=GenerateRequest,
        )


    @staticmethod
    async def generate(
        data: GenerateRequest,
        _: User = Depends(get_current_user),
        session: AsyncSession = Depends(async_session),
    ) -> GenerateResponse:
        """LLM-генерация"""

        return await _generate(
            data=data,
            session=session
        )


    @staticmethod
    async def generate_batch(
        data: BatchGenerateRequest,
        _: User = Depends(get_current_user),
        session: AsyncSession = Depends(async_session),
    ) -> dict[str, Any]:
        """Множественная LLM-генерация"""

        results = []
        for item in data.items:
            try:
                results.append((await _generate(data=item, session=session)).model_dump())

            except HTTPException as exc:
                results.append({
                    "steam_id": item.steam_id,
                    "error": exc.detail,
                    "status_code": exc.status_code
                })

            except Exception as exc:
                logger.exception("Batch generation failed for Steam ID %s", item.steam_id)
                results.append({
                    "steam_id": item.steam_id,
                    "error": type(exc).__name__,
                    "status_code": 500
                })

        return {
            "results": results,
            "count": len(results)
        }


    @staticmethod
    async def generate_variants(
        data: GenerateRequest,
        count: int = 3,
        _: User = Depends(get_current_user),
        session: AsyncSession = Depends(async_session),
    ) -> dict[str, Any]:
        """Много-вариативная LLM-генерация"""

        if not 2 <= count <= 5:
            raise HTTPException(
                status_code=422,
                detail="count must be between 2 and 5"
            )

        variants = []
        for _ in range(count):
            item = data.model_copy(update={"use_cache": False})
            variants.append((await _generate(data=item, session=session)).model_dump())

        selected = max(variants, key=lambda item: item.get("critic_score") or 0)
        comparison = ModelComparison(
            models_compared=[get_llm_gateway().model_name] * len(variants),
            sample_size=1,
            results_json={"variants": variants},
            winner=selected["request_id"],
        )

        session.add(comparison)
        await session.commit()

        return {
            "comparison_internal_id": comparison.internal_id,
            "variants": variants,
            "ensemble": selected,
            "selection_strategy": "highest_critic_score"
        }


    @staticmethod
    async def generate_ensemble(
        data: GenerateRequest,
        _: User = Depends(get_current_user),
        session: AsyncSession = Depends(async_session),
    ) -> dict[str, Any]:
        """Запуск каждого настроенного облачного шлюза с выбором наиболее подходящего варианта"""

        settings = get_settings()
        managers: list[LLMGateway] = []

        for provider, key in (
            ("atria", settings.atria_api_key),
            ("sharellm", settings.sharellm_api_key)
        ):
            if key and key.get_secret_value().strip():
                managers.append(LLMGateway(provider=provider))

        if not managers:
            raise HTTPException(
                status_code=503,
                detail="Configure at least one cloud LLM API key"
            )

        candidates = []
        for manager in managers:
            try:
                candidate = await _generate(
                    data=data.model_copy(update={"use_cache": False}),
                    session=session,
                    llm_manager=manager
                )
                candidate_data = candidate.model_dump()
                candidate_data["provider"] = manager.provider
                candidate_data["model"] = manager.model_name
                candidates.append(candidate_data)

            except HTTPException as exc:
                candidates.append({
                    "provider": manager.provider,
                    "error": exc.detail
                })

        successful = [item for item in candidates if item.get("summary")]

        if not successful:
            raise HTTPException(
                status_code=502,
                detail="All configured LLM gateways failed"
            )

        selected = max(successful, key=lambda item: item.get("critic_score") or 0)
        comparison = ModelComparison(
            models_compared=[manager.provider for manager in managers],
            sample_size=1,
            results_json={"candidates": candidates},
            winner=selected["request_id"],
        )
        session.add(comparison)
        await session.commit()

        return {
            "comparison_internal_id": comparison.internal_id,
            "candidates": candidates,
            "selected": selected,
            "selection_strategy": "highest_critic_score"
        }


class _FinishAgent:
    name = "finish"

    async def process(self, state: dict[str, Any]) -> dict[str, Any]:
        return {"done": True}


def _source_text(data: GenerateRequest) -> str:
    """Получение ключевых данных для запроса"""
    if data.input_text and data.input_text.strip():
        return data.input_text.strip()

    return json.dumps(data.profile, ensure_ascii=False, default=str)


async def _retrieve_context(source: str, session: AsyncSession) -> tuple[list[RetrievedSource], list[str]]:
    """Выполняйте поиск по гибридному индексу (BM25 + Qdrant)"""

    warnings: list[str] = []

    try:
        retrival_service = RetrivalService()
        retriever = await retrival_service.build_retriever(session)
        matches = await retriever.search(source, limit=5)
        sources = [
            RetrievedSource(
                document_id=doc.id,
                source_text=doc.source_text,
                target_text=doc.target_text,
                category=doc.category,
                score=float(score),
            ) for doc, score in matches
        ]

        if not sources:
            warnings.append(
                "Retrieval не вернул релевантных документов; "
                "генерация продолжена без дополнительного контекста."
            )
        return sources, warnings

    except Exception as exc:
        logger.warning("Retrieval unavailable for this request: %s", exc)
        warnings.append(
            "RAG-контекст недоступен (проверьте импорт базы знаний и индекс Qdrant); "
            "использованы исходные данные профиля."
        )
        return [], warnings


async def _generate(
        data: GenerateRequest,
        session: AsyncSession,
        *,
        llm_manager: LLMGateway | None = None,
) -> GenerateResponse:
    """"""

    request_id = str(uuid4())
    manager = llm_manager or get_llm_gateway()

    if data.profile_url:
        settings = get_settings()

        if not settings.steam_api_key or not settings.steam_api_key.get_secret_value().strip():
            raise HTTPException(
                status_code=503,
                detail="Steam Web API key is not configured"
            )

        try:
            steam_profile, _ = await SteamProfileService(session).get_steam_profile_info(data.profile_url)

        except SteamIdentifierError as exc:
            raise HTTPException(
                status_code=422,
                detail=str(exc)
            ) from exc

        except SteamAPIError as exc:
            raise HTTPException(
                status_code=502,
                detail=str(exc)
            ) from exc

        data = data.model_copy(
            update={
                "steam_id": str(steam_profile["steam_id"]),
                "profile": steam_profile,
                "profile_url": None,
            }
        )

    if not data.steam_id:
        raise HTTPException(
            status_code=422,
            detail="Укажите steam_id или profile_url"
        )

    source = _source_text(data)
    payload = data.model_dump(exclude={"use_cache"})

    try:
        configured_model = manager.model_name
    except ValueError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc)
        ) from exc

    payload["provider"] = manager.provider
    payload["model"] = configured_model

    cache_key = hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()

    if data.use_cache:
        cached = await session.scalar(select(Cache).where(Cache.input_key == cache_key))

        if cached:
            cached.hits += 1
            await session.commit()
            return GenerateResponse(
                request_id=request_id,
                steam_id=data.steam_id,
                summary=cached.output,
                mode=data.mode,
                cached=True,
            )

    warnings: list[str] = []
    retrieved_sources: list[RetrievedSource] = []
    profile = data.profile or {}

    if data.mode == "full":
        retrieved_sources, retrieval_warnings = await _retrieve_context(source, session)
        warnings.extend(retrieval_warnings)

    context = "\n\nРелевантные материалы из базы знаний (используй только если они относятся к профилю):\n"
    context += "\n".join(
        f"- Категория: {item.category or 'не указана'}\n  Источник: {item.source_text}\n  Материал: {item.target_text}"
        for item in retrieved_sources
    )
    prompt = (
        "Составь краткое, информативное саммари игрового профиля Steam на русском языке. "
        "Используй только подтверждённые исходными данными факты. Не выдумывай игры, часы, "
        "предпочтения и достижения. Верни только текст саммари.\n\n"
        f"Данные профиля:\n{source}" + (context if retrieved_sources else "")
    )

    try:
        summary = await manager.generate(
            prompt,
            agent_name="generator",
            request_id=request_id
        )

    except Exception as exc:
        logger.exception("Generation failed for request %s", request_id)
        raise HTTPException(
            status_code=502,
            detail=f"LLM gateway request failed: {type(exc).__name__}"
        ) from exc

    validation: dict[str, Any] = {"validation_passed": True, "warnings": []}
    critic_score: float | None = None

    if data.mode == "full":
        state: dict[str, Any] = {
            "request_id": request_id,
            "steam_id": data.steam_id,
            "profile": profile,
            "input_text": source,
            "summary": summary,
            "items": profile.get("games", []) if isinstance(profile, dict) else [],
            "retrieved_sources": [item.model_dump() for item in retrieved_sources],
        }
        supervisor = Supervisor(
            [
                lambda: ValidatorAgent(required_fields=("steam_id",), llm_gateway=manager),
                lambda: CriticAgent(llm_gateway=manager),
                lambda: EditorAgent(llm_gateway=manager),
                _FinishAgent
            ],
            max_iterations=1,
        )

        try:
            state = await supervisor.run(state, request_id=request_id)

        except Exception as exc:
            logger.exception("Agent pipeline failed for request %s", request_id)
            raise HTTPException(
                status_code=502,
                detail="Agent pipeline failed"
            ) from exc

        summary = str(state.get("summary", summary))
        validation = state
        critic_score = state.get("critic_score")
        warnings.extend(str(item) for item in state.get("warnings", []))

    if not summary.strip():
        raise HTTPException(
            status_code=502,
            detail="LLM returned an empty summary"
        )

    if data.use_cache:
        session.add(Cache(input_key=cache_key, output=summary))

        try:
            await session.commit()
        except Exception:
            await session.rollback()
            logger.exception("Could not save generation cache")

    return GenerateResponse(
        request_id=request_id,
        steam_id=data.steam_id,
        summary=summary,
        mode=data.mode,
        cached=False,
        validation_passed=validation.get("validation_passed", True),
        critic_score=critic_score,
        warnings=warnings,
        retrieved_sources=retrieved_sources,
    )