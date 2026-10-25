"""Модульные тесты для агента-валидатора"""

import logging

import pytest

from src.backend.agents import ValidatorAgent


@pytest.mark.asyncio
async def test_validator_accepts_valid_state() -> None:
    validator = ValidatorAgent(required_fields=("steam_id", "summary"), min_text_length=10)

    result = await validator.process(
        {"steam_id": "76561198000000000", "summary": "A fan of strategy games", "items": ["Dota 2"]}
    )

    assert result == {"errors": [], "warnings": [], "validation_passed": True}


@pytest.mark.asyncio
async def test_validator_reports_missing_required_fields() -> None:
    validator = ValidatorAgent(required_fields=("steam_id", "summary"))

    result = await validator.process({"steam_id": " "})

    assert result["validation_passed"] is False
    assert any("steam_id" in error for error in result["errors"])
    assert any("summary" in error for error in result["errors"])


@pytest.mark.asyncio
async def test_validator_checks_minimum_text_length() -> None:
    validator = ValidatorAgent(required_fields=(), min_text_length=10)

    result = await validator.process({"summary": "Too short"})

    assert result["validation_passed"] is False
    assert any("at least 10 characters" in error for error in result["errors"])


@pytest.mark.asyncio
async def test_validator_detects_duplicate_items() -> None:
    validator = ValidatorAgent(required_fields=())

    result = await validator.process({"items": ["Dota 2", "CS2", "dota 2"]})

    assert result["validation_passed"] is False
    assert any("Duplicate items" in error for error in result["errors"])


@pytest.mark.asyncio
async def test_validator_checks_dictionary_terms_case_insensitively() -> None:
    validator = ValidatorAgent(required_fields=(), dictionary={"Dota 2", "Counter-Strike 2"})

    result = await validator.process({"terms": ["dota 2", "Unknown Game"]})

    assert result["validation_passed"] is True
    assert len(result["warnings"]) == 1
    assert "Unknown Game" in result["warnings"][0]


@pytest.mark.asyncio
async def test_optional_llm_check_is_only_a_logged_placeholder(caplog) -> None:
    caplog.set_level(logging.INFO)
    validator = ValidatorAgent(required_fields=(), enable_llm_check=True)

    result = await validator.process({})

    assert result["validation_passed"] is True
    assert any("not configured yet" in warning for warning in result["warnings"])
    assert "placeholder" in caplog.text


def test_validator_rejects_negative_minimum_length() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        ValidatorAgent(min_text_length=-1)
