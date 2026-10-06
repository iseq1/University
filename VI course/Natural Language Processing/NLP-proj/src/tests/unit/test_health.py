"""Smoke-тесты для приложения на FastAPI"""

from fastapi.testclient import TestClient

from src.backend.api import app


def test_healthcheck() -> None:
    """Эндпоинт проверки состояния - должен возвращать статус OK"""
    client = TestClient(app)
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
