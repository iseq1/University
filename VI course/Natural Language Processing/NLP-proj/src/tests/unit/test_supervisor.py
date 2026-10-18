"""Модульные тесты для интерфейса агента и оркестрации со стороны супервизора"""

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.backend.agents import Agent, Supervisor
from src.backend.db import ReasoningLog


class AddProfileAgent(Agent):
    name = "profile"

    async def process(self, state: dict) -> dict:
        return {"profile": {"games": 12}}


class FinishAgent(Agent):
    name = "finish"

    async def process(self, state: dict) -> dict:
        return {"summary": "A strategy-game fan.", "done": True}


class ContinueAgent(Agent):
    name = "continue"

    async def process(self, state: dict) -> dict:
        return {"visited": True}


class FailingAgent(Agent):
    name = "failure"

    async def process(self, state: dict) -> dict:
        raise RuntimeError("agent failed")


def make_session_factory():
    """Создание мок-фабрики сессии"""

    session = MagicMock()
    session.add = MagicMock()
    session.commit = AsyncMock()

    @asynccontextmanager
    async def session_context():
        yield session

    factory = MagicMock(side_effect=session_context)
    return factory, session


@pytest.mark.asyncio
async def test_supervisor_runs_agents_and_stops_when_done() -> None:
    factory, session = make_session_factory()
    supervisor = Supervisor([AddProfileAgent, FinishAgent], factory, max_iterations=4)

    state = await supervisor.run({"steam_id": "123"}, request_id="request-1")

    assert state["profile"] == {"games": 12}
    assert state["summary"] == "A strategy-game fan."
    assert state["done"] is True
    assert state["iteration"] == 1
    assert factory.call_count == 2
    assert session.add.call_count == 2
    assert session.commit.await_count == 2
    assert all(isinstance(call.args[0], ReasoningLog) for call in session.add.call_args_list)
    assert session.add.call_args_list[0].args[0].request_id == "request-1"


@pytest.mark.asyncio
async def test_agents_are_initialized_lazily_and_only_once() -> None:
    factory, _ = make_session_factory()
    agent_factory = MagicMock(side_effect=ContinueAgent)
    supervisor = Supervisor([agent_factory], factory, max_iterations=1)

    assert agent_factory.call_count == 0
    await supervisor.run({"done": True})
    assert agent_factory.call_count == 1
    await supervisor.run({"done": True})
    assert agent_factory.call_count == 1


@pytest.mark.asyncio
async def test_supervisor_stops_at_max_iterations() -> None:
    factory, session = make_session_factory()
    supervisor = Supervisor([ContinueAgent], factory, max_iterations=2)

    state = await supervisor.run({})

    assert state["iteration"] == 2
    assert state["stop_reason"] == "max_iterations_reached"
    assert session.add.call_count == 2


@pytest.mark.asyncio
async def test_supervisor_logs_agent_failure_and_reraises() -> None:
    factory, session = make_session_factory()
    supervisor = Supervisor([FailingAgent], factory, max_iterations=2)

    with pytest.raises(RuntimeError, match="agent failed"):
        await supervisor.run({}, request_id="failed-request")

    log_record = session.add.call_args.args[0]
    assert isinstance(log_record, ReasoningLog)
    assert log_record.status == "failed"
    assert log_record.request_id == "failed-request"
    session.commit.assert_awaited_once()


def test_supervisor_rejects_invalid_iteration_limit() -> None:
    with pytest.raises(ValueError, match="max_iterations"):
        Supervisor([], max_iterations=0)
