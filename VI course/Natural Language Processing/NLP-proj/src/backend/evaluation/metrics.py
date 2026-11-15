"""Метрики генерации текста с опциональной семантической оценкой"""
from __future__ import annotations

from typing import Any


def calculate_metrics(reference: str, prediction: str, include_bertscore: bool = False) -> dict[str, Any]:
    """Расчет лексических метрик"""

    reference, prediction = reference.strip(), prediction.strip()
    if not reference or not prediction:
        raise ValueError(
            "Reference and prediction must be non-empty"
        )

    result: dict[str, Any] = {"exact_match": float(reference.casefold() == prediction.casefold())}

    try:
        from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
        from nltk.translate.chrf_score import sentence_chrf
        from nltk.translate.meteor_score import meteor_score

        ref_tokens, pred_tokens = reference.split(), prediction.split()
        result["bleu"] = float(sentence_bleu(
            [ref_tokens],
            pred_tokens,
            smoothing_function=SmoothingFunction().method1
        ))

        # ROUGE-L F1 based on the longest common subsequence; avoids runtime model downloads.
        def lcs_length(left: list[str], right: list[str]) -> int:
            """"""

            previous = [0] * (len(right) + 1)
            for token in left:
                current = [0]

                for index, other in enumerate(right, start=1):
                    current.append(previous[index - 1] + 1 if token == other else max(previous[index], current[index - 1]))

                previous = current

            return previous[-1]

        common = lcs_length(ref_tokens, pred_tokens)
        precision = common / len(pred_tokens) if pred_tokens else 0.0
        recall = common / len(ref_tokens) if ref_tokens else 0.0
        result["rouge_l"] = (2 * precision * recall / (precision + recall) if precision + recall else 0.0)

        try:
            result["meteor"] = float(meteor_score([ref_tokens], pred_tokens))
        except LookupError:
            result["meteor"] = None
            result["meteor_note"] = "NLTK WordNet corpus is not installed"

        result["chrf"] = float(sentence_chrf(reference, prediction))

    except ImportError as exc:
        raise RuntimeError(
            "Install evaluation dependencies from pyproject.toml"
        ) from exc

    if include_bertscore:
        try:
            from bert_score import score as bert_score
            _, _, f1 = bert_score([prediction], [reference], lang="ru", verbose=False)
            result["bertscore_f1"] = float(f1[0].item())
        except Exception as exc:
            result["bertscore_error"] = str(exc)

    return result
