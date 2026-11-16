"""Контрактные тесты для API-интерфейса, представленного на этапе 12"""
from fastapi.testclient import TestClient

from src.backend.api.main import app
from src.backend.api.schemas.generation import GenerateRequest


def test_stage12_routes_are_registered() -> None:
    paths = app.openapi()["paths"]
    required = {
        "/api/v1/generate",
        "/api/v1/generate/batch",
        "/api/v1/generate/variants",
        "/api/v1/generate/ensemble",
        "/api/v1/steam/profile",
        "/api/v1/evaluate",
        "/api/v1/evaluate/history",
        "/api/v1/requests/{request_id}/reasoning_log",
        "/api/v1/admin/knowledge-base",
        "/api/v1/admin/glossary",
    }
    assert required.issubset(paths)


def test_generate_request_rejects_unknown_mode() -> None:
    try:
        GenerateRequest(steam_id="123", mode="unknown")
    except Exception:
        return
    raise AssertionError("Unsupported generation mode must be rejected")


def test_healthcheck_remains_available() -> None:
    response = TestClient(app).get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_request_accepts_steam_profile_url_without_manual_profile_payload() -> None:
    request = GenerateRequest(profile_url="https://steamcommunity.com/id/example")
    assert request.profile_url.endswith("/example")
    assert request.steam_id is None
