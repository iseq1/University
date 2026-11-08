"""Модульные тесты для поддерживаемых облачных LLM-шлюзов и трассировки вызовов"""

import pytest

from src.backend.gateways.llm import LLMGateway


class FakeClient:
    model = "fake-model"

    def __init__(self, response="generated text", error=None):
        self.response = response
        self.error = error

    async def call(self, prompt):
        if self.error:
            raise self.error
        return self.response


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return self._payload


class FakeAsyncClient:
    calls = []
    response = FakeResponse({"choices": [{"message": {"content": "hello from gateway"}}]})

    def __init__(self, timeout):
        self.timeout = timeout

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None

    async def post(self, url, headers, json):
        self.calls.append({"url": url, "headers": headers, "json": json})
        return self.response


@pytest.mark.asyncio
async def test_manager_routes_to_client_and_logs(monkeypatch):
    import src.backend.gateways.llm.gateway as module

    calls = []

    async def fake_log(**kwargs):
        calls.append(kwargs)

    monkeypatch.setattr(module, "log_llm_call", fake_log)
    manager = LLMGateway(provider="test", client=FakeClient(" hello "))
    result = await manager.generate("private prompt", agent_name="editor", request_id="req-1")

    assert result == "hello"
    assert len(calls) == 1
    assert calls[0]["status"] == "success"
    assert calls[0]["agent_name"] == "editor"
    assert calls[0]["request_id"] == "req-1"
    assert calls[0]["response"] == " hello "


@pytest.mark.asyncio
async def test_manager_logs_failure_and_reraises(monkeypatch):
    import src.backend.gateways.llm.gateway as module

    calls = []

    async def fake_log(**kwargs):
        calls.append(kwargs)

    monkeypatch.setattr(module, "log_llm_call", fake_log)
    manager = LLMGateway(provider="test", client=FakeClient(error=RuntimeError("offline")))

    with pytest.raises(RuntimeError, match="offline"):
        await manager.generate("prompt", agent_name="critic")

    assert calls[0]["status"] == "error"
    assert calls[0]["response"] is None


@pytest.mark.asyncio
async def test_atria_client_sends_openai_compatible_request(monkeypatch):
    import src.backend.gateways.llm.client.astria as client
    import src.backend.gateways.llm.client.base as base_client


    FakeAsyncClient.calls = []
    monkeypatch.setattr(base_client.httpx, "AsyncClient", FakeAsyncClient)
    client = client.AtriaClient("atria-key", "Atria-Dawn", "https://api.atria-asi.ai/v1")

    assert await client.call("test prompt") == "hello from gateway"
    call = FakeAsyncClient.calls[-1]
    assert call["url"] == "https://api.atria-asi.ai/v1/chat/completions"
    assert call["headers"]["Authorization"] == "Bearer atria-key"
    assert call["json"]["model"] == "Atria-Dawn"
    assert call["json"]["messages"][0]["content"] == "test prompt"


@pytest.mark.asyncio
async def test_sharellm_client_uses_configured_model_and_endpoint(monkeypatch):
    import src.backend.gateways.llm.client.share_llm as client
    import src.backend.gateways.llm.client.base as base_client

    FakeAsyncClient.calls = []
    monkeypatch.setattr(base_client.httpx, "AsyncClient", FakeAsyncClient)
    client = client.ShareLLMClient(
        "share-key", "deepseek-v4.1-flash", "https://sharellm.net/v1"
    )

    assert await client.call("hello") == "hello from gateway"
    call = FakeAsyncClient.calls[-1]
    assert call["url"] == "https://sharellm.net/v1/chat/completions"
    assert call["headers"]["Authorization"] == "Bearer share-key"
    assert call["json"]["model"] == "deepseek-v4.1-flash"


def test_manager_requires_atria_key(monkeypatch):
    import src.backend.gateways.llm.gateway as module

    class Settings:
        atria_api_key = None

    monkeypatch.setattr(module, "get_settings", lambda: Settings())
    manager = LLMGateway(provider="atria")
    with pytest.raises(ValueError, match="Параметр ATRIA_API_KEY обязателен, если LLM_PROVIDER=atria"):
        manager._get_client()


def test_manager_rejects_removed_local_and_paid_providers():
    manager = LLMGateway(provider="openai")
    with pytest.raises(ValueError, match="Поддерживаемы облачные шлюзы: atria, sharellm, sber"):
        manager._get_client()


def test_manager_rejects_unknown_provider():
    manager = LLMGateway(provider="not-a-provider")
    with pytest.raises(ValueError, match="Неподдерживаемый LLM_PROVIDER"):
        manager._get_client()
