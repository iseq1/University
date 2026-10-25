"""Агент-судья на базе LLM с детерминированным резервным механизмом"""

import json
import logging
import math
from typing import Any

from src.backend.agents import Agent

logger = logging.getLogger(__name__)

CRITIC_FEW_SHOT_PROMPT = '''You are a strict evaluator of a generated Steam profile summary.
Return only a valid JSON object with these keys:
- relevance: number from 1 to 10
- completeness: number from 1 to 10
- style: number from 1 to 10
- reasoning: short explanation
- suggestions: array of improvement suggestions
- passed: boolean

Evaluate only facts supported by the supplied profile data. Do not reward invented details.

Example:
Input profile: {"games": ["Portal 2", "Half-Life 2"], "summary": "The player enjoys narrative puzzle games."}
Output: {"relevance": 9, "completeness": 8, "style": 9, "reasoning": "The summary reflects both listed games without adding unsupported claims.", "suggestions": [], "passed": true}

Now evaluate this profile:
{payload}
'''


class CriticAgent(Agent):
    """Класс, описывающий агента-критика"""

    name = "critic"


    def __init__(self, pass_threshold: float = 6.0) -> None:

        if not 1.0 <= pass_threshold <= 10.0:
            raise ValueError(
                "pass_threshold must be between 1 and 10"
            )

        self.pass_threshold = pass_threshold


    async def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """Оценка текущего результата"""

        payload = {
            "profile": state.get("profile", {}),
            "summary": state.get("summary", ""),
        }

        prompt = CRITIC_FEW_SHOT_PROMPT.replace(
            "{payload}", json.dumps(payload, ensure_ascii=False, default=str)
        )

        try:
            raw_response = await self._call_llm(prompt)
            evaluation = self._parse_response(raw_response)
        except Exception as exc:
            logger.warning("Critic evaluation failed; using fallback score 5.0: %s", exc)
            evaluation = {
                "relevance": 5.0,
                "completeness": 5.0,
                "style": 5.0,
                "reasoning": "Fallback evaluation was used because the LLM response was unavailable or invalid.",
                "suggestions": ["Repeat evaluation when the LLM integration is available."],
                "passed": False,
            }

        scores = [evaluation[key] for key in ("relevance", "completeness", "style")]
        score = round(sum(scores) / len(scores), 2)
        passed = bool(evaluation.get("passed", score >= self.pass_threshold)) and score >= self.pass_threshold

        logger.info("Critic evaluation completed: score=%.2f passed=%s", score, passed)
        return {
            "critic_score": score,
            "critic_reasoning": evaluation["reasoning"],
            "critic_suggestions": evaluation["suggestions"],
            "critic_passed": passed,
            "critic_dimensions": {
                "relevance": evaluation["relevance"],
                "completeness": evaluation["completeness"],
                "style": evaluation["style"],
            },
        }


    async def _call_llm(self, prompt: str) -> str:
        """Заглушка для реального клиента LLM"""
        logger.info("LLM call placeholder invoked for CriticAgent (prompt_length=%s)", len(prompt))
        raise NotImplementedError("LLM integration is scheduled for next stage")


    @staticmethod
    def _parse_response(response: str | dict[str, Any]) -> dict[str, Any]:
        """Парсинг LLM-ответа"""

        data = response if isinstance(response, dict) else json.loads(response)
        if not isinstance(data, dict):
            raise ValueError(
                "Critic response must be a JSON object"
            )

        scores: dict[str, float] = {}
        for key in ("relevance", "completeness", "style"):
            value = data.get(key)

            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(
                    f"'{key}' must be a number between 1 and 10"
                )

            if not math.isfinite(value) or not 1 <= value <= 10:
                raise ValueError(
                    f"'{key}' must be a number between 1 and 10"
                )

            scores[key] = float(value)

        reasoning = data.get("reasoning", "")
        suggestions = data.get("suggestions", [])
        passed = data.get("passed")

        if not isinstance(reasoning, str):
            raise ValueError(
                "'reasoning' must be a string"
            )

        if not isinstance(suggestions, list) or not all(isinstance(item, str) for item in suggestions):
            raise ValueError(
                "'suggestions' must be a list of strings"
            )

        if not isinstance(passed, bool):
            raise ValueError(
                "'passed' must be a boolean"
            )

        return {
            **scores,
            "reasoning": reasoning,
            "suggestions": suggestions,
            "passed": passed
        }


Critic = CriticAgent
