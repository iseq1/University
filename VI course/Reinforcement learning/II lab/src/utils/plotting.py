"""Утилиты визуализации"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_convergence(history, output_dir="results/plots"):
    """
    Строит график сходимости Value Iteration.
    :param history: Максимальное изменение ценности на каждой итерации
    :param output_dir: Каталог для сохранения графика
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    iterations = np.arange(1, len(history) + 1)

    plt.figure(figsize=(9, 5))
    plt.semilogy(iterations, history, label="Value Iteration")
    plt.axhline(
        y=1e-6,
        linestyle="--",
        label="Порог сходимости",
    )

    plt.xlabel("Номер итерации")
    plt.ylabel("Максимальное изменение ценности")
    plt.title("Сходимость алгоритма Value Iteration")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path / "value_iteration_convergence.png", dpi=150)
    plt.close()


def plot_parameter_results(results, output_dir="results/plots"):
    """
    Строит графики зависимости результатов от gamma и theta.

    :param results: DataFrame с результатами экспериментов.
    :param output_dir: Каталог сохранения графиков.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    metrics = [
        ("time_seconds", "Время выполнения, с", "time"),
        ("iterations", "Число итераций", "iterations"),
        ("success_rate", "Вероятность успеха", "success_rate"),
    ]

    for parameter in ["gamma", "theta"]:
        subset = results[results["parameter"] == parameter]

        for metric, ylabel, filename in metrics:
            fig, ax = plt.subplots(figsize=(8, 5))

            for algorithm_name in subset["algorithm"].unique():
                data = subset[
                    subset["algorithm"] == algorithm_name
                ].sort_values("parameter_value")

                ax.plot(
                    data["parameter_value"],
                    data[metric],
                    marker="o",
                    label=algorithm_name,
                )

            if parameter == "theta":
                ax.set_xscale("log")

            ax.set_xlabel(parameter)
            ax.set_ylabel(ylabel)
            ax.set_title(f"Влияние {parameter} на {ylabel.lower()}")
            ax.grid(True, alpha=0.3)
            ax.legend()
            fig.tight_layout()

            fig.savefig(
                output_path / f"{parameter}_{filename}.png",
                dpi=150,
            )
            plt.close(fig)
