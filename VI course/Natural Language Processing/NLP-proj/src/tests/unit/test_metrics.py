"""Модульные тесты для метрик"""

import pytest

from src.backend.evaluation import calculate_metrics


def test_exact_match_and_lexical_metrics():
    result = calculate_metrics("A player likes strategy games", "A player likes strategy games")
    assert result["exact_match"] == 1.0
    assert result["bleu"] > 0.9
    assert result["rouge_l"] == pytest.approx(1.0)
    assert result["chrf"] > 0.9


def test_empty_text_is_rejected():
    with pytest.raises(ValueError):
        calculate_metrics("", "summary")
