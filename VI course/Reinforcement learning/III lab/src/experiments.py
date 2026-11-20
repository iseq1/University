"""Экспериментальный запуск и формирование результатов лабораторной работы."""

import argparse
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src.config import GAMMA, N_EPISODES, N_EVALUATION_EPISODES, RANDOM_SEED
from src.plugins.environment import FrozenLakeEnvironment
from src.plugins.algorithms import (
    GreedyHandler,
    EpsilonGreedyHandler,
    OffPolicyHandler,
)


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
RESULTS = DOCS / "results"
IMAGES = DOCS / "images"


def moving_average(values, window=250):
    values = np.asarray(values, dtype=float)
    if len(values) == 0:
        return values
    window = min(window, len(values))
    return np.convolve(values, np.ones(window) / window, mode="valid")


def save_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def run_one(handler, algorithm_name, episodes, eval_episodes, seed, epsilon=None):
    env = FrozenLakeEnvironment()
    try:
        if algorithm_name == "epsilon_greedy":
            q_values, visits, rewards = handler.train(
                env, epsilon=epsilon, n_episodes=episodes, gamma=GAMMA, seed=seed
            )
        else:
            q_values, visits, rewards = handler.train(
                env, n_episodes=episodes, gamma=GAMMA, seed=seed
            )

        success_rate, average_steps = handler.evaluate(
            env, q_values, n_episodes=eval_episodes, seed=seed + 100_000
        )
        return {
            "algorithm": algorithm_name,
            "epsilon": epsilon,
            "seed": seed,
            "episodes": episodes,
            "evaluation_episodes": eval_episodes,
            "success_rate": float(success_rate),
            "average_steps": float(average_steps),
            "training_reward_mean": float(np.mean(rewards)) if rewards else 0.0,
            "q_values": q_values.tolist(),
            "visits": visits.tolist(),
            "episode_rewards": [float(x) for x in rewards],
        }
    finally:
        env.close()


def aggregate_runs(runs):
    metrics = ("success_rate", "average_steps", "training_reward_mean")
    result = {"algorithm": runs[0]["algorithm"], "epsilon": runs[0]["epsilon"]}
    for metric in metrics:
        values = [run[metric] for run in runs]
        result[metric] = float(np.mean(values))
        result[metric + "_std"] = float(np.std(values, ddof=1)) if len(values) > 1 else 0.0
    result["seeds"] = [run["seed"] for run in runs]
    return result


def plot_comparison(summary):
    names = [row["label"] for row in summary]
    success = [row["success_rate"] * 100 for row in summary]
    errors = [row["success_rate_std"] * 100 for row in summary]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(names, success, yerr=errors, capsize=5)
    ax.set_ylabel("Доля успешных эпизодов, %")
    ax.set_title("Сравнение алгоритмов Monte Carlo Control")
    ax.set_ylim(0, 100)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(IMAGES / "algorithm_comparison.png", dpi=160)
    plt.close(fig)


def plot_learning_curves(representative_runs):
    fig, ax = plt.subplots(figsize=(10, 5))
    for label, run in representative_runs.items():
        curve = moving_average(run["episode_rewards"], window=250)
        if len(curve):
            ax.plot(np.arange(len(curve)) + min(250, len(run["episode_rewards"])),
                    curve, label=label)
    ax.set_xlabel("Эпизод обучения")
    ax.set_ylabel("Средняя награда (скользящее среднее, окно 250)")
    ax.set_title("Динамика награды в процессе обучения")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(IMAGES / "learning_curves.png", dpi=160)
    plt.close(fig)


def plot_budget_sweep(budget_rows):
    fig, ax = plt.subplots(figsize=(9, 5))
    for algorithm in ("greedy_es", "epsilon_greedy", "off_policy_wis"):
        rows = [row for row in budget_rows if row["algorithm"] == algorithm]
        rows.sort(key=lambda row: row["episodes"])
        labels = {
            "greedy_es": "Жадная + ES",
            "epsilon_greedy": "ε-жадная",
            "off_policy_wis": "Off-policy + WIS",
        }
        ax.plot(
            [row["episodes"] for row in rows],
            [row["success_rate"] * 100 for row in rows],
            marker="o",
            label=labels[algorithm],
        )
    ax.set_xlabel("Количество обучающих эпизодов")
    ax.set_ylabel("Доля успешных эпизодов, %")
    ax.set_title("Влияние продолжительности обучения")
    ax.set_ylim(0, 100)
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(IMAGES / "episode_budget.png", dpi=160)
    plt.close(fig)


def plot_epsilon_sweep(epsilon_rows):
    fig, ax = plt.subplots(figsize=(8, 5))
    x = [row["epsilon"] for row in epsilon_rows]
    y = [row["success_rate"] * 100 for row in epsilon_rows]
    ax.plot(x, y, marker="o")
    ax.set_xlabel("Значение ε")
    ax.set_ylabel("Доля успешных эпизодов, %")
    ax.set_title("Влияние параметра ε на ε-жадный Monte Carlo Control")
    ax.set_ylim(0, 100)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(IMAGES / "epsilon_sweep.png", dpi=160)
    plt.close(fig)


def write_report(summary, epsilon_rows, budget_rows, all_runs, episodes, eval_episodes, seeds):
    rows = "\n".join(
        f"| {r['label']} | {r['success_rate']*100:.2f} ± {r['success_rate_std']*100:.2f} | "
        f"{r['average_steps']:.2f} ± {r['average_steps_std']:.2f} |"
        for r in summary
    )
    eps_rows = "\n".join(
        f"| {r['epsilon']:.2f} | {r['success_rate']*100:.2f} | {r['average_steps']:.2f} |"
        for r in epsilon_rows
    )
    budget_table = "\n".join(
        f"| {r['algorithm_label']} | {r['episodes']} | {r['success_rate']*100:.2f} | {r['average_steps']:.2f} |"
        for r in budget_rows
    )
    action_names = ["LEFT", "DOWN", "RIGHT", "UP"]
    q_sections = []
    for algorithm_key, title in [
        ("greedy_es", "Жадная + Exploring Starts"),
        ("epsilon_greedy", "ε-жадная"),
        ("off_policy_wis", "Off-policy + Weighted IS"),
    ]:
        q = all_runs[algorithm_key][0]["q_values"]
        q_rows = "\n".join(
            f"| {state} | " + " | ".join(f"{value:.3f}" for value in values) + " |"
            for state, values in enumerate(q)
        )
        q_sections.append(
            f"### {title} (первое случайное зерно)\n\n"
            f"| Состояние | " + " | ".join(action_names) + " |\n"
            f"|---:|---:|---:|---:|---:|\n{q_rows}"
        )
    q_tables = "\n\n".join(q_sections)
    report = f"""# Лабораторная работа № 3. Исследование метода Монте-Карло

## Цель работы

Исследовать методы получения оптимальной стратегии принятия решений на основе метода Монте-Карло в среде FrozenLake, реализовать методы с жадной, ε-жадной и распределённой (off-policy) стратегиями и сравнить их экспериментальные характеристики.

## Среда и параметры эксперимента

Используется FrozenLake-v1, карта 4×4, скользкая поверхность (`is_slippery=True`). Агент получает награду 1 за достижение цели и 0 за остальные переходы. Коэффициент дисконтирования γ = {GAMMA}.

Количество эпизодов обучения: {episodes}. Количество независимых эпизодов оценки: {eval_episodes}. Случайные зерна: {seeds}. При оценке используется жадная целевая стратегия без дополнительного исследования.

## Исследуемые алгоритмы

### 1. Жадный Monte Carlo Control с Exploring Starts

В начале каждого обучающего эпизода выбирается случайная допустимая стартовая пара «состояние — действие». После первого действия агент выбирает жадное действие на основании текущих оценок Q(s,a). Оценки обновляются усреднением возвратов по первому посещению пары «состояние — действие».

### 2. ε-жадный Monte Carlo Control

При выборе действия с вероятностью ε агент исследует среду, выбирая случайное действие, а с вероятностью 1−ε использует действие с максимальной оценкой Q(s,a). В основном сравнении используется ε = 0.10. Дополнительно исследуется влияние ε.

### 3. Off-policy Monte Carlo Control с Weighted Importance Sampling

Для генерации эпизодов используется поведенческая стратегия с равномерным распределением вероятностей между действиями. Целевая стратегия является детерминированной жадной стратегией. Для корректировки оценок используется взвешенное выборочное усреднение с коэффициентом важности W. Обновление выполняется в обратном порядке по эпизоду; обработка префикса прекращается, если выбранное поведенческой стратегией действие не совпадает с действием целевой стратегии.

## Методика оценки

Основная метрика — Success Rate, то есть доля эпизодов, в которых агент достиг целевого состояния. Дополнительно рассчитывается среднее количество шагов до завершения эпизода. Для уменьшения влияния случайности результаты основного сравнения усредняются по нескольким случайным зернам. Эпизоды оценки не используются для обновления Q-таблиц.

## Результаты основного сравнения

| Алгоритм | Успешные эпизоды, % (среднее ± σ) | Среднее число шагов (среднее ± σ) |
|---|---:|---:|
{rows}

![Сравнение алгоритмов](images/algorithm_comparison.png)

## Влияние параметра ε

| ε | Успешные эпизоды, % | Среднее число шагов |
|---:|---:|---:|
{eps_rows}

![Влияние epsilon](images/epsilon_sweep.png)

## Влияние количества обучающих эпизодов

Для оценки влияния длительности обучения каждый алгоритм дополнительно запускался с разным бюджетом эпизодов. Для этой серии использовалось первое зерно из основного набора.

| Алгоритм | Эпизоды обучения | Успешные эпизоды при оценке, % | Среднее число шагов |
|---|---:|---:|---:|
{budget_table}

![Влияние числа эпизодов](images/episode_budget.png)

## Динамика обучения

На графике показано скользящее среднее награды за обучающие эпизоды. Эта метрика характеризует поведение исследующего агента во время обучения и не заменяет независимую оценку итоговой политики.

![Динамика обучения](images/learning_curves.png)

## Итоговые таблицы Q(s,a)

Ниже приведены оценки качества действий для первого случайного зерна. Полные таблицы и счётчики посещений для всех запусков сохранены в `results/experiment_results.json`.

{q_tables}

## Итоговые таблицы Q(s,a)

Ниже приведены оценки качества действий для первого случайного зерна. Полные таблицы и счётчики посещений для всех запусков сохранены в `results/experiment_results.json`.

{q_tables}

## Анализ результатов

При сравнении следует учитывать различия в механизмах исследования пространства состояний. Exploring Starts обеспечивает исследование начальных пар «состояние — действие», ε-жадная стратегия продолжает исследование на каждом шаге, а off-policy подход формирует данные равномерной поведенческой стратегией и корректирует оценки относительно целевой политики.

Weighted Importance Sampling может характеризоваться высокой дисперсией весов, особенно при длинных последовательностях совпадений поведения с целевой стратегией. Поэтому результат off-policy метода зависит от числа эпизодов и случайного зерна. Результаты эксперимента следует интерпретировать с учётом стандартного отклонения между запусками.

## Заключение

В работе реализованы и экспериментально сопоставлены три варианта Monte Carlo Control: жадный метод с Exploring Starts, ε-жадный метод и off-policy метод с Weighted Importance Sampling. Сравнение выполнено по доле успешных прохождений и среднему количеству шагов, а также дополнено исследованием влияния ε и динамики обучения.

Итоговый вывод о наиболее эффективном алгоритме необходимо формулировать по полученным экспериментальным значениям, учитывая не только средний результат, но и его устойчивость при разных случайных зернах.
"""
    (DOCS / "REPORT.md").write_text(report, encoding="utf-8")


def run_experiments(episodes=N_EPISODES, eval_episodes=N_EVALUATION_EPISODES,
                    seeds=None, epsilons=None, budgets=None):
    seeds = seeds or [RANDOM_SEED, RANDOM_SEED + 1, RANDOM_SEED + 2]
    epsilons = epsilons or [0.02, 0.05, 0.10, 0.20, 0.30]
    budgets = budgets or sorted(set([max(1000, episodes // 10), episodes // 2, episodes]))
    RESULTS.mkdir(parents=True, exist_ok=True)
    IMAGES.mkdir(parents=True, exist_ok=True)

    algorithms = [
        ("greedy_es", "Жадная + Exploring Starts", GreedyHandler(), None),
        ("epsilon_greedy", "ε-жадная (ε=0.10)", EpsilonGreedyHandler(), 0.10),
        ("off_policy_wis", "Off-policy + Weighted IS", OffPolicyHandler(), None),
    ]

    all_runs = {}
    summary = []
    for key, label, handler, epsilon in algorithms:
        runs = [
            run_one(handler, key, episodes, eval_episodes, seed, epsilon)
            for seed in seeds
        ]
        all_runs[key] = runs
        aggregate = aggregate_runs(runs)
        aggregate["label"] = label
        summary.append(aggregate)

    epsilon_rows = []
    for epsilon in epsilons:
        run = run_one(
            EpsilonGreedyHandler(), "epsilon_greedy",
            episodes, eval_episodes, seeds[0], epsilon
        )
        epsilon_rows.append({
            "epsilon": epsilon,
            "success_rate": run["success_rate"],
            "average_steps": run["average_steps"],
        })

    budget_rows = []
    for budget in budgets:
        if budget <= 0:
            continue
        for key, label, handler, epsilon in algorithms:
            run = run_one(handler, key, budget, eval_episodes, seeds[0], epsilon)
            budget_rows.append({
                "algorithm": key,
                "algorithm_label": label,
                "episodes": budget,
                "success_rate": run["success_rate"],
                "average_steps": run["average_steps"],
            })

    save_json({"summary": summary, "epsilon_sweep": epsilon_rows,
               "episode_budget_sweep": budget_rows,
               "runs": all_runs}, RESULTS / "experiment_results.json")

    with (RESULTS / "summary.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "label", "success_rate", "success_rate_std",
            "average_steps", "average_steps_std",
            "training_reward_mean", "training_reward_mean_std",
        ])
        writer.writeheader()
        for row in summary:
            writer.writerow({key: row[key] for key in writer.fieldnames})

    representatives = {
        "Жадная + ES": all_runs["greedy_es"][0],
        "ε-жадная": all_runs["epsilon_greedy"][0],
        "Off-policy + WIS": all_runs["off_policy_wis"][0],
    }
    plot_comparison(summary)
    plot_learning_curves(representatives)
    plot_epsilon_sweep(epsilon_rows)
    plot_budget_sweep(budget_rows)
    write_report(summary, epsilon_rows, budget_rows, all_runs, episodes, eval_episodes, seeds)

    print("\nИТОГОВОЕ СРАВНЕНИЕ")
    for row in summary:
        print(
            f"{row['label']}: success={row['success_rate']*100:.2f}% "
            f"± {row['success_rate_std']*100:.2f} п.п.; "
            f"steps={row['average_steps']:.2f} ± {row['average_steps_std']:.2f}"
        )
    print(f"\nРезультаты сохранены в: {DOCS}")
    return summary


def main():
    parser = argparse.ArgumentParser(description="Эксперименты Monte Carlo / FrozenLake")
    parser.add_argument("--episodes", type=int, default=N_EPISODES)
    parser.add_argument("--eval-episodes", type=int, default=N_EVALUATION_EPISODES)
    parser.add_argument("--seeds", type=int, nargs="+", default=[
        RANDOM_SEED, RANDOM_SEED + 1, RANDOM_SEED + 2
    ])
    parser.add_argument("--epsilons", type=float, nargs="+",
                        default=[0.02, 0.05, 0.10, 0.20, 0.30])
    parser.add_argument("--budgets", type=int, nargs="+",
                        default=[1000, 3000, 5000, 10_000, 100_000])
    args = parser.parse_args()
    run_experiments(
        args.episodes,
        args.eval_episodes,
        args.seeds,
        args.epsilons,
        args.budgets
    )


if __name__ == "__main__":
    main()
