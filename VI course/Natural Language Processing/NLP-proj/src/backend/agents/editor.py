"""Агент-редактор, который применяет к краткому изложению замечания валидатора и критика"""

import json
import logging
from typing import Any

from src.backend.agents import Agent

logger = logging.getLogger(__name__)

EDITOR_PROMPT_TEMPLATE = """You edit a generated summary of a Steam profile.
Correct the summary using the validation errors and critic suggestions below.
Preserve factual accuracy: use only information supported by the profile.
Do not invent games, statistics, preferences, or other facts.
Return only a JSON object with one string field: \"summary\".

Profile data:
{profile}

Current summary:
{summary}

Validation errors:
{errors}

Critic suggestions:
{suggestions}
"""


class EditorAgent(Agent):
    """Класс, описывающий агента-редактора"""

    name = "editor"


    def __init__(self):
        self.request_id = None


    async def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """Внесите правки в текущее резюме, если имеются конструктивные замечания"""
        self.request_id = str(state.get("request_id", ""))

        errors = state.get("errors", [])
        suggestions = state.get("critic_suggestions", [])
        errors = errors if isinstance(errors, list) else [str(errors)]
        suggestions = suggestions if isinstance(suggestions, list) else [str(suggestions)]

        if not errors and not suggestions:
            logger.info("Editor skipped: no validation errors or critic suggestions")
            return {"editor_changed": False}

        original_summary = state.get("summary", "")
        prompt = EDITOR_PROMPT_TEMPLATE.format(
            profile=json.dumps(state.get("profile", {}), ensure_ascii=False, default=str),
            summary=str(original_summary),
            errors=json.dumps(errors, ensure_ascii=False),
            suggestions=json.dumps(suggestions, ensure_ascii=False),
        )

        try:
            raw_response = await self._call_llm(prompt)
            edited_summary = self._parse_response(raw_response)
        except Exception as exc:
            logger.warning("Editor correction failed; preserving original summary: %s", exc)
            return {
                "editor_changed": False,
                "editor_error": str(exc),
            }

        changed = edited_summary != original_summary
        logger.info("Editor completed: changed=%s", changed)
        return {
            "summary": edited_summary,
            "editor_changed": changed,
            "editor_error": None,
        }


    async def _call_llm(self, prompt: str) -> str:
        """Формирование оценки с помощью настроенного LLM-провайдера"""
        from src.backend.gateways.llm import get_llm_gateway

        return await get_llm_gateway().generate(
            prompt=prompt,
            agent_name=self.name,
            request_id=str(getattr(self, "request_id", "")),
        )


    @staticmethod
    def _parse_response(response: str | dict[str, Any]) -> str:
        """Распарсить ответ редактора и извлечь непустую строку-резюме"""

        data = response if isinstance(response, dict) else json.loads(response)

        if not isinstance(data, dict):
            raise ValueError("Ответ агента-редактора должен быть JSON-объектом")

        summary = data.get("summary")

        if not isinstance(summary, str) or not summary.strip():
            raise ValueError("Ответ агента-редактора должен содержать НЕ пустую строку 'summary'")

        return summary.strip()


Editor = EditorAgent
