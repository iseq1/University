"""Файл реализации супервизора - инициализирует агентов по мере необходимости (ленивая инициализация) и фиксирует этапы выполнения"""

import json
import logging
from collections.abc import Callable, Sequence
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.backend.agents import Agent, AgentFactory
from src.backend.db import ReasoningLog, Session


logger = logging.getLogger(__name__)
SessionFactory = Callable[[], Any]


class Supervisor:
    """Класс, описывающий супервизора агентов"""


    def __init__(
        self,
        agent_factories: Sequence[AgentFactory],
        session_factory: SessionFactory | async_sessionmaker[AsyncSession] | None = None,
        max_iterations: int = 3,
    ) -> None:

        if max_iterations < 1:
            raise ValueError("Максимальное количество итераций должно быть не менее 1")

        self._session = Session()
        self._agent_factories = list(agent_factories)
        self._session_factory = session_factory or self._session.get_session_factory()
        self.max_iterations = max_iterations
        self._agents: list[Agent] | None = None


    def _get_agents(self) -> list[Agent]:
        """Создание экземпляра агентов"""

        if not self._agents:
            self._agents = [factory() for factory in self._agent_factories]
            names = [agent.name for agent in self._agents]

            if len(names) != len(set(names)):
                raise ValueError("Имена агентов должны быть уникальными")

        return self._agents


    async def run(
        self,
        state: dict[str, Any],
        request_id: str | None = None,
    ) -> dict[str, Any]:
        """Запуск конвейера агентов"""

        request_id = request_id or str(uuid4())
        state.setdefault("request_id", request_id)
        state.setdefault("iteration", 0)

        agents = self._get_agents()
        if not agents:
            state["done"] = True
            state["stop_reason"] = "no_agents_registered"
            return state

        for iteration in range(1, self.max_iterations + 1):
            state["iteration"] = iteration

            for agent in agents:
                if state.get("done") is True:
                    break

                started_at = datetime.now(timezone.utc)
                input_summary = self._summarize(state)

                try:

                    updates = await agent.process(state)

                    if not isinstance(updates, dict):

                        raise TypeError(
                            f"Agent '{agent.name}' must return a dictionary, "
                            f"got {type(updates).__name__}"
                        )

                    state.update(updates)
                    await self._save_log(
                        request_id=request_id,
                        agent_name=agent.name,
                        input_summary=input_summary,
                        output_summary=self._summarize(updates),
                        started_at=started_at,
                        status="success",
                        iteration=iteration,
                    )
                    logger.info(
                        "Agent '%s' completed request %s (iteration %s)",
                        agent.name,
                        request_id,
                        iteration,
                    )

                except Exception as exc:

                    await self._save_log(
                        request_id=request_id,
                        agent_name=agent.name,
                        input_summary=input_summary,
                        output_summary=str(exc)[:2000],
                        started_at=started_at,
                        status="failed",
                        iteration=iteration,
                    )
                    logger.exception("Agent '%s' failed for request %s", agent.name, request_id)
                    state["error"] = str(exc)
                    state["done"] = True
                    state["stop_reason"] = "agent_error"
                    raise

            if state.get("done") is True:
                state.setdefault("stop_reason", "completed")
                break

        else:
            state["stop_reason"] = "max_iterations_reached"

        return state


    async def _save_log(
        self,
        *,
        request_id: str,
        agent_name: str,
        input_summary: str,
        output_summary: str,
        started_at: datetime,
        status: str,
        iteration: int,
    ) -> None:
        """Логирование записи о выполнении агента"""

        async with self._session_factory() as session:
            session.add(
                ReasoningLog(
                    request_id=request_id,
                    agent_name=agent_name,
                    input_summary=input_summary,
                    output_summary=output_summary,
                    model_name=None,
                    parameters={"iteration": iteration},
                    started_at=started_at,
                    finished_at=datetime.now(timezone.utc),
                    status=status,
                )
            )
            await session.commit()


    @staticmethod
    def _summarize(value: Any, max_length: int = 2000) -> str:
        """Преобразовать данные о состоянии в безопасное для логирования JSON-представление"""
        try:
            summary = json.dumps(value, ensure_ascii=False, default=str)
        except (TypeError, ValueError):
            summary = str(value)
        return summary[:max_length]
