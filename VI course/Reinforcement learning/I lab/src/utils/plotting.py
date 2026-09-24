"""
Файл содержит реализацию функций для построения графиков
"""
import os

import matplotlib.pyplot as plt

ALGORITHMS = [
    "Greedy",
    "Epsilon-Greedy",
    "UCB",
    "Gradient"
]


def plot_parameter_reward(
    parameter_values: list,
    results: dict,
    parameter_name: str,
    title: str,
    save_path: str =None
):
    """
    График зависимости итоговой средней награды от параметра алгоритма
    :param parameter_values: Целевой параметр
    :param results: Список с результатами
    :param parameter_name: Наименование параметра
    :param title: Заголовок графика
    :param save_path: Путь для сохранения
    :return:
    """

    final_rewards = [
        results[value]["average_rewards"][-1]
        for value in parameter_values
    ]

    plt.figure(figsize=(10, 6))
    plt.plot(
        parameter_values,
        final_rewards,
        marker="o"
    )

    plt.title(title)
    plt.xlabel(parameter_name)
    plt.ylabel("Итоговая средняя награда")

    plt.grid(True)
    plt.legend()

    if save_path is not None:
        os.makedirs(
            os.path.dirname(save_path),
            exist_ok=True
        )

        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()


def plot_parameter_optimal_action(
    parameter_values,
    results,
    parameter_name,
    title,
    save_path: str = None
):
    """
    График зависимости доли выбора оптимального действия от параметра алгоритма
    :param parameter_values: Целевой параметр
    :param results: Список с результатами
    :param parameter_name: Наименование параметра
    :param title: Заголовок графика
    :param save_path: Путь для сохранения
    :return:
    """

    final_optimal_rates = [
        results[value]["optimal_action_rate"][-1]
        for value in parameter_values
    ]

    plt.figure(figsize=(10, 6))

    plt.plot(
        parameter_values,
        final_optimal_rates,
        marker="o"
    )

    plt.title(title)
    plt.xlabel(parameter_name)
    plt.ylabel("Доля выбора оптимального действия")

    plt.grid(True)
    plt.legend()

    if save_path is not None:
        os.makedirs(
            os.path.dirname(save_path),
            exist_ok=True
        )

        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()


def plot_parameter_learning_curves(
    parameter_values,
    results,
    parameter_name,
    title,
    save_path: str = None
):
    """
    График изменения средней награды по эпизодам для разных значений параметра.
    :param parameter_values: Целевой параметр
    :param results: Список с результатами
    :param parameter_name: Наименование параметра
    :param title: Заголовок графика
    :param save_path: Путь для сохранения
    :return:
    """

    plt.figure(figsize=(10, 6))

    for value in parameter_values:

        plt.plot(
            results[value]["average_rewards"],
            label=f"{parameter_name} = {value}"
        )

    plt.title(title)
    plt.xlabel("Эпизод")
    plt.ylabel("Средняя награда")

    plt.grid(True)
    plt.legend()

    if save_path is not None:
        os.makedirs(
            os.path.dirname(save_path),
            exist_ok=True
        )

        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()


def plot_parameter_results(
    parameter_values: list,
    results: dict,
    parameter_name: str,
    title: str,
    save_path: str = None
):
    """
    Строит график влияния параметра одного алгоритма
    :param parameter_values: Целевой параметр
    :param results: Список с результатами
    :param parameter_name: Наименование параметра
    :param title: Заголовок графика
    :param save_path: Путь для сохранения
    :return:
    """

    plot_parameter_reward(
        parameter_values=parameter_values,
        results=results,
        parameter_name=parameter_name,
        title=f"{title}: влияние {parameter_name} на среднюю награду",
        save_path="".join([save_path, "reward.png"]),
    )

    plot_parameter_optimal_action(
        parameter_values=parameter_values,
        results=results,
        parameter_name=parameter_name,
        title=f"{title}: влияние {parameter_name} на выбор оптимального действия",
        save_path="".join([save_path, "optimal_action.png"]),
    )

    plot_parameter_learning_curves(
        parameter_values=parameter_values,
        results=results,
        parameter_name=parameter_name,
        title=f"{title} при различных значениях {parameter_name}",
        save_path="".join([save_path, "learning_curves.png"]),
    )


def plot_algorithm_comparison(
    results,
    title,
    metric="average_rewards",
    save_path: str = None
):
    """
    Сравнивает несколько алгоритмов по одной метрике
    :param results: Список с результатами
    :param metric: Целевая метрика
    :param title: Заголовок графика
    :param save_path: Путь для сохранения
    :return:
    """

    plt.figure(figsize=(10, 6))

    for algorithm in ALGORITHMS:

        plt.plot(
            results[algorithm][metric],
            label=algorithm
        )

    plt.title(title)
    plt.xlabel("Эпизод")

    if metric == "average_rewards":
        plt.ylabel("Средняя награда")

    elif metric == "optimal_action_rate":
        plt.ylabel("Доля выбора оптимального действия")

    plt.grid(True)
    plt.legend()

    if save_path is not None:
        os.makedirs(
            os.path.dirname(save_path),
            exist_ok=True
        )

        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()


def plot_algorithms_diff_results(baseline_results, save_path: str = None):
    """
    Сравнение алгоритмов по целевым метрикам
    :param baseline_results: Список результатов
    :param save_path: Путь для сохранения
    :return:
    """

    plot_algorithm_comparison(
        results=baseline_results,
        title="Сравнение алгоритмов",
        metric="average_rewards",
        save_path="".join([save_path, "average_rewards"])
    )

    plot_algorithm_comparison(
        results=baseline_results,
        title="Выбор оптимального действия",
        metric="optimal_action_rate",
        save_path="".join([save_path, "optimal_action_rate"])
    )


def plot_action_count(
    action_counts,
    results,
    metric,
    title,
    save_path: str = None
):
    """
    Строит зависимость выбранной метрики от количества рычагов.
    :param action_counts: Список рычагов
    :param results: Список с результатами
    :param metric: Целевая метрика
    :param title: Заголовок графика
    :param save_path: Путь для сохранения
    :return:
    """

    plt.figure(figsize=(10, 6))

    for algorithm in ALGORITHMS:

        values = [
            results[count][algorithm][metric][-1]
            for count in action_counts
        ]

        plt.plot(
            action_counts,
            values,
            marker="o",
            label=algorithm
        )

    plt.title(title)
    plt.xlabel("Количество рычагов")

    if metric == "average_rewards":
        plt.ylabel("Средняя награда")

    elif metric == "optimal_action_rate":
        plt.ylabel("Доля выбора оптимального действия")

    plt.grid(True)
    plt.legend()

    if save_path is not None:
        os.makedirs(
            os.path.dirname(save_path),
            exist_ok=True
        )

        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()


def plot_levers_diff(levers_list, action_count_results, save_path: str = None):
    """
    Строит зависимость выбранной метрики от количества рычагов.
    :param levers_list: Список рычагов
    :param action_count_results: Список с результатами
    :param save_path: Путь для сохранения
    :return:
    """

    plot_action_count(
        action_counts=levers_list,
        results=action_count_results,
        metric="average_rewards",
        title="Влияние количества рычагов на среднюю награду",
        save_path="".join([save_path, "average_rewards"])
    )

    plot_action_count(
        action_counts=levers_list,
        results=action_count_results,
        metric="optimal_action_rate",
        title="Влияние количества рычагов на выбор оптимального действия",
        save_path="".join([save_path, "optimal_action_rate"])
    )

