"""Модульные тесты для EditorAgent."""

import json

import pytest

from src.backend.agents import EditorAgent


@pytest.mark.asyncio
async def test_editor_applies_feedback(monkeypatch):
    agent = EditorAgent()
    edited = "The player enjoys puzzle and narrative games."

    async def fake_call_llm(prompt):
        assert "Missing playtime" in prompt
        assert "Mention the player's main genres" in prompt
        return json.dumps({"summary": edited})

    monkeypatch.setattr(agent, "_call_llm", fake_call_llm)
    result = await agent.process({
        "profile": {"games": ["Portal 2"]},
        "summary": "A gamer.",
        "errors": ["Missing playtime"],
        "critic_suggestions": ["Mention the player's main genres"],
    })

    assert result["summary"] == edited
    assert result["editor_changed"] is True
    assert result["editor_error"] is None


@pytest.mark.asyncio
async def test_editor_skips_llm_when_no_feedback(monkeypatch):
    agent = EditorAgent()

    async def unexpected_call(prompt):
        raise AssertionError("LLM must not be called without feedback")

    monkeypatch.setattr(agent, "_call_llm", unexpected_call)
    result = await agent.process({"summary": "A concise summary.", "errors": [], "critic_suggestions": []})

    assert result == {"editor_changed": False}


@pytest.mark.asyncio
async def test_editor_preserves_summary_when_llm_unavailable(monkeypatch):
    agent = EditorAgent()

    async def failing_call(prompt):
        raise RuntimeError("provider unavailable")

    monkeypatch.setattr(agent, "_call_llm", failing_call)
    result = await agent.process({"summary": "Original summary", "errors": ["Too short"]})

    assert "summary" not in result
    assert result["editor_changed"] is False
    assert "provider unavailable" in result["editor_error"]


@pytest.mark.parametrize("response", [
    "not json",
    "[]",
    "{\"summary\": \"   \"}",
    "{\"summary\": 123}",
])
def test_editor_rejects_invalid_response(response):
    with pytest.raises((ValueError, json.JSONDecodeError)):
        EditorAgent._parse_response(response)


def test_editor_accepts_dict_response():
    assert EditorAgent._parse_response({"summary": " Edited summary "}) == "Edited summary"
