"""Модульные тесты для CriticAgent"""

import json

import pytest

from src.backend.agents import CriticAgent


@pytest.mark.asyncio
async def test_critic_process_uses_valid_llm_response(monkeypatch):
    agent = CriticAgent(pass_threshold=6.0)
    response = {
        "relevance": 9,
        "completeness": 8,
        "style": 7,
        "reasoning": "The summary matches the profile.",
        "suggestions": ["Mention playtime."],
        "passed": True,
    }

    async def fake_call_llm(prompt):
        assert "Steam profile summary" in prompt
        return json.dumps(response)

    monkeypatch.setattr(agent, "_call_llm", fake_call_llm)
    result = await agent.process({"profile": {"games": ["Portal 2"]}, "summary": "Puzzle fan."})

    assert result["critic_score"] == 8.0
    assert result["critic_passed"] is True
    assert result["critic_reasoning"] == response["reasoning"]
    assert result["critic_suggestions"] == ["Mention playtime."]
    assert result["critic_dimensions"] == {"relevance": 9.0, "completeness": 8.0, "style": 7.0}


@pytest.mark.asyncio
async def test_critic_falls_back_to_score_five(monkeypatch):
    agent = CriticAgent()

    async def failing_call(prompt):
        raise RuntimeError("provider unavailable")

    monkeypatch.setattr(agent, "_call_llm", failing_call)
    result = await agent.process({"summary": "A summary"})

    assert result["critic_score"] == 5.0
    assert result["critic_passed"] is False
    assert result["critic_suggestions"]


@pytest.mark.parametrize("response", [
    "not json",
    '{"relevance": 11, "completeness": 8, "style": 7, "reasoning": "x", "suggestions": [], "passed": true}',
    '{"relevance": 8, "completeness": 8, "style": 7, "reasoning": "x", "suggestions": "none", "passed": true}',
])
def test_parse_response_rejects_invalid_payload(response):
    with pytest.raises((ValueError, json.JSONDecodeError)):
        CriticAgent._parse_response(response)


def test_parse_response_accepts_valid_json():
    parsed = CriticAgent._parse_response({
        "relevance": 8,
        "completeness": 7,
        "style": 9,
        "reasoning": "Good summary.",
        "suggestions": [],
        "passed": True,
    })
    assert parsed["relevance"] == 8.0
    assert parsed["passed"] is True
