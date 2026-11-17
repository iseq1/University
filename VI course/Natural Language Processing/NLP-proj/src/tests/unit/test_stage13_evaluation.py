"""Модульные тесты для вспомогательных функций оценки этапа 13 и API-контрактов"""
import json

import pytest
from fastapi.testclient import TestClient

from src.backend.api import app
from src.backend.api import EvaluationBatchRequest
from src.backend.evaluation import EvaluationRunner, SUPPORTED_MODES


def test_stage13_routes_are_registered() -> None:
    paths = app.openapi()["paths"]
    assert "/api/v1/evaluate/compare" in paths
    assert "/api/v1/evaluate/batch" in paths
    assert "/api/v1/evaluate/tasks/{task_id}" in paths


def test_supported_evaluation_modes_are_complete() -> None:
    assert SUPPORTED_MODES == ("baseline", "+dict", "+rag", "+agents", "+ensemble")


def test_evaluation_batch_request_accepts_required_sample_sizes() -> None:
    for size in (20, 50, 100):
        request = EvaluationBatchRequest(models=["atria"], sample_size=size)
        assert request.sample_size == size


def test_evaluation_batch_request_rejects_unsupported_sample_size() -> None:
    with pytest.raises(ValueError):
        EvaluationBatchRequest(models=["atria"], sample_size=30)


def test_load_dataset_validates_source_and_reference(tmp_path) -> None:
    path = tmp_path / "samples.json"
    path.write_text(json.dumps([{"source_text": "profile", "target_text": "summary"}]), encoding="utf-8")
    assert EvaluationRunner.load_dataset(path) == [{"source_text": "profile", "target_text": "summary", "category": ""}]


def test_load_dataset_rejects_invalid_schema(tmp_path) -> None:
    path = tmp_path / "samples.json"
    path.write_text(json.dumps([{"source_text": "profile"}]), encoding="utf-8")
    with pytest.raises(ValueError):
        EvaluationRunner.load_dataset(path)


def test_prompt_adds_dictionary_or_rag_context() -> None:
    base = EvaluationRunner._prompt("sample profile", "baseline")
    enriched = EvaluationRunner._prompt("sample profile", "+dict", "term: definition")
    assert "term: definition" not in base
    assert "term: definition" in enriched


def test_healthcheck_remains_available() -> None:
    response = TestClient(app).get("/healthz")
    assert response.status_code == 200
