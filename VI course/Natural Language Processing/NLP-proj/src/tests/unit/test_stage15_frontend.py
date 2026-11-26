"""Контрактные тесты для фронтенд-клиента API"""

import httpx
import pytest

from src.frontend.utils import APIClient, APIError


def test_api_client_adds_bearer_token(monkeypatch):
    def fake_request(self, method, url, **kwargs):
        assert method == "GET"
        assert url == "/auth/me"
        assert kwargs["headers"] == {"Authorization": "Bearer test-token"}
        return httpx.Response(200, json={"role": "user"}, request=httpx.Request("GET", "http://localhost:8000/auth/me"))

    monkeypatch.setattr(httpx.Client, "request", fake_request)
    assert APIClient(token="test-token").get("/auth/me") == {"role": "user"}


def test_api_client_formats_api_error(monkeypatch):
    def fake_request(self, method, url, **kwargs):
        return httpx.Response(403, json={"detail": "Forbidden"}, request=httpx.Request("GET", "http://localhost:8000/test"))

    monkeypatch.setattr(httpx.Client, "request", fake_request)
    with pytest.raises(APIError, match="HTTP 403: Forbidden"):
        APIClient().get("/test")
