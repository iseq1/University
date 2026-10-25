"""Агент проверки на основе правил для общего состояния обработки"""

import logging
from collections.abc import Iterable, Mapping
from typing import Any

from src.backend.agents import Agent


logger = logging.getLogger(__name__)


class ValidatorAgent(Agent):
    """Класс, описывающий агента-валидатор"""

    name = "validator"


    def __init__(
        self,
        required_fields: Iterable[str] = ("steam_id",),
        min_text_length: int = 10,
        dictionary: Iterable[str] | None = None,
        enable_llm_check: bool = False,
    ) -> None:

        if min_text_length < 0:
            raise ValueError("min_text_length must be non-negative")

        self.required_fields = tuple(required_fields)
        self.min_text_length = min_text_length
        self.dictionary = {term.casefold() for term in dictionary} if dictionary is not None else None
        self.enable_llm_check = enable_llm_check


    async def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """Валидация состояния"""

        errors: list[str] = []
        warnings: list[str] = []

        empty_errors = self._validate_empty_error(
            state=state,
            required_fields=self.required_fields
        )

        min_length_errors = self._validate_min_length_error(
            state=state,
            min_text_length=self.min_text_length
        )

        duplicate_errors = self._validate_duplicate_error(
            state=state
        )

        errors.extend([
            *empty_errors,
            *min_length_errors,
            *duplicate_errors
        ])

        unknown_term_warnings = self._validate_unknown_term_warning(
            state=state,
            dictionary=self.dictionary
        )

        warnings.extend([
            *unknown_term_warnings,
        ])

        if self.enable_llm_check:
            logger.info("LLM validation check is a placeholder; no external model was called.")
            warnings.append("LLM validation is not configured yet.")

        validation_passed = not errors
        logger.info(
            "Validation completed: passed=%s, errors=%s, warnings=%s",
            validation_passed,
            len(errors),
            len(warnings),
        )

        return {
            "errors": errors,
            "warnings": warnings,
            "validation_passed": validation_passed,
        }


    @staticmethod
    def _find_duplicates(items: Any) -> list[str]:
        """Выполнение проверки на вхождение дубликатов"""
        if not isinstance(items, (list, tuple)):
            return []

        seen: set[str] = set()
        duplicates: set[str] = set()
        for item in items:
            key = ValidatorAgent._stable_key(item)
            if key in seen:
                duplicates.add(key)
            seen.add(key)
        return sorted(duplicates)


    @staticmethod
    def _stable_key(value: Any) -> str:
        """Создание ключ сравнения для типичных JSON-подобных значений"""

        if isinstance(value, Mapping):
            return repr(sorted((str(key), ValidatorAgent._stable_key(item)) for key, item in value.items()))

        if isinstance(value, (list, tuple)):
            return repr([ValidatorAgent._stable_key(item) for item in value])

        return str(value).casefold() if isinstance(value, str) else repr(value)


    @staticmethod
    def _validate_empty_error(state: dict[str, Any], required_fields: Iterable[str]) -> list[str]:
        """Валидация пустых значений"""
        empty_errors = []

        for field in required_fields:
            value = state.get(field)

            if value is None or (isinstance(value, str) and not value.strip()):
                empty_errors.append(
                    f"Required field '{field}' is missing or empty."
                )

        return empty_errors


    @staticmethod
    def _validate_min_length_error(state: dict[str, Any], min_text_length: int) -> list[str]:
        """Валидация минимальной длины поля"""
        min_length_errors = []

        for field in ("input_text", "summary"):
            value = state.get(field)

            if isinstance(value, str) and value.strip() and len(value.strip()) < min_text_length:
                min_length_errors.append(
                    f"Field '{field}' must contain at least {min_text_length} characters."
                )

        return min_length_errors


    @staticmethod
    def _validate_duplicate_error(state: dict[str, Any]) -> list[str]:
        """Валидация дублей"""
        duplicate_errors = []

        duplicates = ValidatorAgent._find_duplicates(state.get("items"))
        if duplicates:
            duplicate_errors.append(
                f"Duplicate items found: {duplicates}."
            )

        return duplicate_errors


    @staticmethod
    def _validate_unknown_term_warning(state: dict[str, Any], dictionary) -> list[str]:
        """Валидация незнакомых терминов"""
        unknown_term_warnings = []

        terms = state.get("terms")
        if all([
            dictionary is not None,
            isinstance(terms, (list, tuple, set)),
        ]):
            unknown_terms = sorted(
                {str(term) for term in terms if str(term).casefold() not in dictionary}
            )

            if unknown_terms:
                unknown_term_warnings.append(
                    f"Terms not found in the dictionary: {unknown_terms}."
                )

        return unknown_term_warnings


# Элиас для вызывающих сторон
Validator = ValidatorAgent
