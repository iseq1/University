"""Лог метаданных о вызовах LLM"""

import logging
import uuid

from src.backend.utils.utils import custom_hash

logger = logging.getLogger(__name__)


async def log_llm_call(
    *,
    request_id: str,
    agent_name: str,
    model_name: str,
    provider: str,
    prompt: str,
    response: str | None,
    latency_ms: float,
    status: str,
    tokens_used: int | None = None
) -> None:
    """Лог записи о LLM-вызове"""

    try:
        from src.backend.db import LLMCall, Session

        async with Session().get_session() as session:
            session.add(
                LLMCall(
                    request_id=request_id or str(uuid.uuid4()),
                    agent_name=agent_name,
                    model_name=model_name,
                    provider=provider,
                    prompt_hash=custom_hash(prompt) or "",
                    response_hash=custom_hash(response),
                    tokens_used=tokens_used,
                    latency_ms=latency_ms,
                    status=status,
                )
            )
            await session.commit()

    except Exception as e:
        logger.exception(
            "Не удалось сохранить метаданные вызова LLM"
        )
