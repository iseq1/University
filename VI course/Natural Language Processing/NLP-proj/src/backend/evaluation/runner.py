"""Многократно используемый конвейер для офлайн- и онлайн-оценки, предназначенный для сравнения моделей и режимов работы"""
from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any, Sequence
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.agents import CriticAgent, EditorAgent, Supervisor, ValidatorAgent
from src.backend.core import get_settings
from src.backend.db import EvaluationResult, Glossary, ModelComparison
from src.backend.evaluation.metrics import calculate_metrics
from src.backend.gateways.llm.gateway import LLMGateway
from src.backend.retrieval import RetrivalService


logger = logging.getLogger(__name__)
SUPPORTED_MODES = ("baseline", "+dict", "+rag", "+agents", "+ensemble")
SUPPORTED_PROVIDERS = ("sber", "atria", "sharellm")
DEFAULT_DATASET = Path("data/generated/knowledge_base_test.json")


class _FinishAgent:
    name = "finish"

    async def process(self, state: dict[str, Any]) -> dict[str, Any]:
        return {"done": True}


class EvaluationRunner:
    """Прогон детерминированной выборки через выбранные облачные модели и системные режимы"""


    def __init__(self, session: AsyncSession, *, include_bertscore: bool = False) -> None:
        self.session = session
        self.include_bertscore = include_bertscore

    @staticmethod
    def load_dataset(path: str | Path = DEFAULT_DATASET) -> list[dict[str, str]]:
        """Загрузка эталонных примеров из JSON-списка, содержащего поля source_text/target_text"""

        dataset_path = Path(path)
        if not dataset_path.exists():
            raise FileNotFoundError(
                f"Evaluation dataset not found: {dataset_path}"
            )

        data = json.loads(dataset_path.read_text(encoding="utf-8"))
        if not isinstance(data, list) or not data:
            raise ValueError(
                "Evaluation dataset must be a non-empty JSON list"
            )

        valid = []
        for index, item in enumerate(data):
            if not isinstance(item, dict) or not item.get("source_text") or not item.get("target_text"):
                raise ValueError(
                    f"Dataset item {index} must contain source_text and target_text"
                )

            valid.append({
                "source_text": str(item["source_text"]),
                "target_text": str(item["target_text"]),
                "category": str(item.get("category") or "")}
            )

        return valid

    @staticmethod
    def configured_providers(requested: Sequence[str]) -> list[str]:
        """Установка конфигурации LLM-провайдеров"""

        settings = get_settings()
        configured = {
            "sber": bool(settings.sber_auth_key and settings.sber_auth_key.get_secret_value().strip()),
            "atria": bool(settings.atria_api_key and settings.atria_api_key.get_secret_value().strip()),
            "sharellm": bool(settings.sharellm_api_key and settings.sharellm_api_key.get_secret_value().strip()),
        }

        providers = list(dict.fromkeys(requested))
        invalid = sorted(set(providers) - set(SUPPORTED_PROVIDERS))

        if invalid:
            raise ValueError(
                f"Unsupported providers: {', '.join(invalid)}"
            )

        unavailable = [
            provider
            for provider in providers
            if not configured[provider]
        ]

        if unavailable:
            raise ValueError(
                f"API keys are not configured for: {', '.join(unavailable)}"
            )

        if not providers:
            raise ValueError(
                "At least one configured provider is required"
            )

        return providers


    async def _dictionary_context(self, source: str, limit: int = 8) -> str:
        """Получение контекста в виде словаря"""

        rows = (await self.session.execute(select(Glossary).order_by(Glossary.internal_id))).scalars().all()
        query = source.casefold()

        tokens = {
            token.strip(".,:;!?()[]{}\"'")
            for token in query.split()
            if len(token) > 2
        }

        ranked = []
        for row in rows:
            term = row.term.casefold()
            score = int(term in query) * 3 + sum(1 for token in tokens if token in term)

            if score:
                ranked.append((score, row))

        ranked.sort(key=lambda item: item[0], reverse=True)

        return "\n".join(f"- {row.term}: {row.definition}" for _, row in ranked[:limit])


    async def _rag_context(self, source: str, limit: int = 5) -> str:
        """Получение rag-контекста"""

        retrival_service = RetrivalService()
        retriever = await retrival_service.build_retriever(self.session)
        matches = await retriever.search(source, limit=limit)

        if not matches:
            return ""

        return "\n\n".join(
            f"- Пример: {doc.source_text}\n  Эталон: {doc.target_text}"
            for doc, _ in matches
        )

    @staticmethod
    def _prompt(source: str, mode: str, context: str = "") -> str:
        """Формирование промпта"""

        prompt = (
            "Составь краткое и информативное саммари игрового профиля Steam на русском языке. "
            "Используй только факты из исходных данных; не выдумывай игры, часы, предпочтения "
            "или достижения. Верни только саммари.\n\n"
            f"Данные профиля:\n{source}"
        )

        if context:
            label = "Справочная информация" if mode == "+dict" else "Релевантные примеры из RAG"
            prompt += f"\n\n{label}:\n{context}\nИспользуй контекст только если он действительно относится к профилю."

        return prompt


    async def _generate_one(self, source: str, mode: str, manager: LLMGateway, request_id: str) -> str:
        """Единичная генерация"""

        context = ""
        if mode == "+dict":
            context = await self._dictionary_context(source=source)
        elif mode == "+rag":
            context = await self._rag_context(source=source)

        prompt = self._prompt(
            source=source,
            mode=mode,
            context=context
        )

        summary = await manager.generate(prompt, agent_name="evaluation_generator", request_id=request_id)
        if mode == "+agents":
            state: dict[str, Any] = {
                "request_id": request_id,
                "steam_id": "evaluation-sample",
                "profile": {"raw": source},
                "input_text": source,
                "summary": summary,
                "items": [],
            }

            supervisor = Supervisor(
                [
                    lambda: ValidatorAgent(required_fields=("steam_id",), llm_gateway=manager),
                    lambda: CriticAgent(llm_gateway=manager),
                    lambda: EditorAgent(llm_gateway=manager),
                    _FinishAgent
                ],
                max_iterations=1,
            )

            state = await supervisor.run(state, request_id=request_id)
            summary = str(state.get("summary", summary))

        return summary.strip()


    async def _generate_ensemble(self, source: str, managers: list[LLMGateway], request_id: str) -> tuple[str, str]:
        """Множественная генерация"""

        candidates: list[tuple[float, str, str]] = []

        for manager in managers:
            candidate = await manager.generate(
                self._prompt(source, "baseline"),
                agent_name="evaluation_ensemble",
                request_id=request_id
            )

            judged = await CriticAgent(llm_gateway=manager).process({
                "request_id": request_id,
                "profile": {"raw": source},
                "summary": candidate,
            })

            candidates.append((float(judged.get("critic_score") or 0), manager.provider, candidate))

        _, provider, summary = max(candidates, key=lambda item: item[0])

        return summary.strip(), provider


    async def evaluate(
        self,
        *,
        providers: Sequence[str],
        modes: Sequence[str],
        sample_size: int,
        dataset_path: str | Path = DEFAULT_DATASET,
        seed: int = 42,
    ) -> dict[str, Any]:
        """Получение оценки"""

        if sample_size not in (20, 50, 100):
            raise ValueError(
                "sample_size must be one of: 20, 50, 100"
            )

        modes = list(dict.fromkeys(modes))
        invalid_modes = sorted(set(modes) - set(SUPPORTED_MODES))
        if invalid_modes:
            raise ValueError(
                f"Unsupported modes: {', '.join(invalid_modes)}"
            )

        providers = self.configured_providers(providers)
        dataset = self.load_dataset(dataset_path)
        if len(dataset) < sample_size:
            raise ValueError(
                f"Dataset contains {len(dataset)} samples; {sample_size} requested"
            )

        import random
        rng = random.Random(seed)
        samples = rng.sample(dataset, sample_size)

        managers = {
            provider: LLMGateway(provider=provider)
            for provider in providers
        }

        results: list[dict[str, Any]] = []
        for mode in modes:
            target_providers = ["ensemble"] if mode == "+ensemble" else providers

            for provider in target_providers:
                started = time.perf_counter()
                per_sample: list[dict[str, Any]] = []
                manager = managers[providers[0]]

                for index, sample in enumerate(samples):
                    request_id = f"eval-{uuid4()}"

                    if mode == "+ensemble":
                        prediction, selected_provider = await self._generate_ensemble(
                            source=sample["source_text"],
                            managers=[managers[p] for p in providers],
                            request_id=request_id
                        )

                    else:
                        manager = managers[provider]
                        prediction = await self._generate_one(
                            source=sample["source_text"],
                            mode=mode,
                            manager=manager,
                            request_id=request_id
                        )

                    metrics = calculate_metrics(
                        reference=sample["target_text"],
                        prediction=prediction,
                        include_bertscore=self.include_bertscore
                    )

                    per_sample.append({
                        "index": index,
                        "reference": sample["target_text"],
                        "prediction": prediction,
                        "metrics": metrics,
                    })

                elapsed = time.perf_counter() - started
                metric_names = sorted(
                    {
                        key
                        for row in per_sample
                        for key, value in row["metrics"].items()
                        if isinstance(value, (int, float))
                    }
                )

                aggregate = {
                    key: round(
                        sum(
                            float(row["metrics"][key])
                            for row in per_sample
                            if isinstance(row["metrics"].get(key), (int, float))
                        ) / max(
                            1,
                            sum(
                                isinstance(row["metrics"].get(key), (int, float))
                                for row in per_sample
                            )
                        ), 6
                    )
                    for key in metric_names
                }

                model_name = f"ensemble({','.join(providers)})" if mode == "+ensemble" else manager.model_name
                record = EvaluationResult(
                    model_name=model_name,
                    mode=mode,
                    sample_size=sample_size,
                    metrics_json=aggregate,
                    evaluation_time=elapsed,
                )

                self.session.add(record)
                results.append({
                    "provider": provider,
                    "model_name": model_name,
                    "mode": mode,
                    "sample_size": sample_size,
                    "metrics": aggregate,
                    "evaluation_time": round(elapsed, 3),
                    "samples": per_sample,
                })

                await self.session.flush()
            await self.session.commit()

        comparison_key = "chrf"
        winner_row = max(results, key=lambda item: item["metrics"].get(comparison_key, -1)) if results else None
        comparison = ModelComparison(
            models_compared=[f"{item['provider']}:{item['mode']}" for item in results],
            sample_size=sample_size,
            results_json={
                "seed": seed,
                "dataset": str(dataset_path),
                "results": [
                    {
                        key: value
                        for key, value in item.items()
                        if key != "samples"
                    } for item in results
                ]
            },
            winner=(f"{winner_row['provider']}:{winner_row['mode']}" if winner_row else None),
        )

        self.session.add(comparison)
        await self.session.commit()

        return {
            "comparison_internal_id": comparison.internal_id,
            "sample_size": sample_size,
            "seed": seed,
            "providers": providers,
            "modes": modes,
            "winner_metric": comparison_key,
            "winner": comparison.winner,
            "results": results
        }
