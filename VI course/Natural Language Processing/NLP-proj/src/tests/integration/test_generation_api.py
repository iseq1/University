"""Интеграционные тесты API с использованием TestClient и mocked-шлюза LLM"""
from collections.abc import AsyncGenerator
from typing import Any

from fastapi.testclient import TestClient

from src.backend.api.deps import get_current_user
from src.backend.api.main import app
from src.backend.db import User, Session
from src.backend.api.routes import GenerationRouter


class FakeSession:
    def __init__(self) -> None:
        self.added: list[Any] = []

    async def scalar(self, statement: Any) -> None:
        return None

    def add(self, value: Any) -> None:
        self.added.append(value)

    async def commit(self) -> None:
        return None


class FakeLLMManager:
    provider = "atria"
    model_name = "Atria-Dawn-test"

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        assert "Portal 2" in prompt
        return "Игрок предпочитает головоломки и сюжетные игры."


async def override_user() -> User:
    return User(
        id=1,
        email="test@example.com",
        username="tester",
        hashed_password="not-used",
        role="user",
        is_active=True
    )


async def override_session() -> AsyncGenerator[FakeSession, None]:
    yield FakeSession()


# def test_baseline_generation_endpoint_uses_mocked_llm(monkeypatch) -> None:
#     # monkeypatch.setattr(GenerationRouter, "get_llm_manager", lambda: FakeLLMManager())
#     app.dependency_overrides[get_current_user] = override_user
#     app.dependency_overrides[Session().get_session()] = override_session
#     try:
#         response = TestClient(app).post("/api/v1/generate", json={
#             "steam_id": "76561198000000000",
#             "profile": {"games": [{"name": "Portal 2", "playtime_hours": 42}]},
#             "mode": "baseline",
#             "use_cache": False,
#         })
#     finally:
#         app.dependency_overrides.clear()
#
#     assert response.status_code == 200
#     payload = response.json()
#     assert payload["mode"] == "baseline"
#     assert payload["summary"] == "Игрок предпочитает головоломки и сюжетные игры."
#     assert payload["cached"] is False
