"""Проведение воспроизводимой оценки на основе сводных данных Steam и экспорт отчетов в формате JSON/CSV"""
from __future__ import annotations

import argparse
import asyncio
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.backend.db import Session
from src.backend.evaluation import EvaluationRunner, SUPPORTED_MODES
from src.backend.core import get_settings
from src.scripts.base import BaseScript


class EvaluationScript(BaseScript):
    """Скрипты для изучения"""

    @staticmethod
    def parse_csv(value: str) -> list[str]:
        """Парсинг CSV-файла"""

        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]


    def build_parser(self) -> argparse.ArgumentParser:
        """Формирование парсера"""

        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--providers", default=None, help="Comma-separated: sber,atria,sharellm")
        parser.add_argument("--modes", default=",".join(SUPPORTED_MODES), help="Comma-separated evaluation modes")
        parser.add_argument("--sample-sizes", default="20,50,100", help="Comma-separated sample sizes")
        parser.add_argument("--dataset", default=str(self._get_output_dir() / "knowledge_base_test.json"))
        parser.add_argument("--output-dir", default=str(self._get_output_dir() / "reports/evaluation"))
        parser.add_argument("--seed", type=int, default=42)
        parser.add_argument("--bertscore", action="store_true", help="Enable optional BERTScore (may download a model)")

        return parser


    async def run(self, args: argparse.Namespace) -> dict[str, Any]:
        """Прогон скрипта"""

        settings = get_settings()

        if args.providers:
            providers = self.parse_csv(args.providers)

        else:
            configured = []

            if settings.sber_auth_key and settings.sber_auth_key.get_secret_value().strip():
                configured.append("sber")

            if settings.atria_api_key and settings.atria_api_key.get_secret_value().strip():
                configured.append("atria")

            if settings.sharellm_api_key and settings.sharellm_api_key.get_secret_value().strip():
                configured.append("sharellm")

            providers = configured

        modes = self.parse_csv(args.modes)
        sizes = [int(item) for item in self.parse_csv(args.sample_sizes)]

        if not sizes or any(size not in (20, 50, 100) for size in sizes):
            raise ValueError(
                "--sample-sizes accepts only 20,50,100"
            )

        output_dir = Path(args.output_dir) / datetime.now(timezone.utc).strftime("%Y-%m-%d %H-%M")
        output_dir.mkdir(parents=True, exist_ok=True)

        all_runs = []

        session_generator = Session().get_session()
        session = await anext(session_generator)

        try:
            runner = EvaluationRunner(
                session,
                include_bertscore=args.bertscore,
            )

            for size in sizes:
                print(
                    f"Starting evaluation: sample_size={size}, "
                    f"providers={providers}, modes={modes}"
                )

                result = await runner.evaluate(
                    providers=providers,
                    modes=modes,
                    sample_size=size,
                    dataset_path=args.dataset,
                    seed=args.seed,
                )

                all_runs.append(result)

                (output_dir / f"evaluation_{size}.json").write_text(
                    json.dumps(result, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )

        finally:
            await session_generator.aclose()

        flat = []
        for run_result in all_runs:
            for row in run_result["results"]:
                flat.append({
                    "provider": row["provider"],
                    "model_name": row["model_name"],
                    "mode": row["mode"],
                    "sample_size": row["sample_size"],
                    "evaluation_time": row["evaluation_time"],
                    **row["metrics"],
                })

        if flat:
            fields = list(dict.fromkeys(key for row in flat for key in row))
            with (output_dir / "results.csv").open("w", encoding="utf-8-sig", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                writer.writerows(flat)

        report_lines = [
            "# Evaluation summary", "", "| Provider | Mode | Samples | chrF | ROUGE-L | BLEU | METEOR | Exact Match | Time, s |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|"
        ]

        for row in flat:
            report_lines.append(
                f"| {row['provider']} | {row['mode']} | {row['sample_size']} | "
                f"{row.get('chrf', '')} | {row.get('rouge_l', '')} | {row.get('bleu', '')} | "
                f"{row.get('meteor', '')} | {row.get('exact_match', '')} | {row['evaluation_time']} |"
            )

        (output_dir / "summary.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

        return {
            "output_dir": str(output_dir),
            "runs": len(all_runs),
            "rows": len(flat)
        }


    def main(self) -> None:
        args = self.build_parser().parse_args()
        result = asyncio.run(self.run(args))
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    EvaluationScript().main()
