"""
Файл, содержащий все необходимые утилиты для запуска экспериментов
"""
from typing import Any

import torch


def calculate_average_reward(rewards: list[float]) -> list[float]:
    """Вычисляет среднюю накопленную награду на каждом шаге эксперимента"""

    average_rewards = []
    total_reward = 0

    for episode, reward in enumerate(rewards, start=1):
        total_reward += reward
        average_rewards.append(total_reward / episode)

    return average_rewards


def calculate_optimal_action_rate(actions: list[int], optimal_action: int) -> list[float]:
    """Вычисляет долю выбора оптимального действия на каждом шаге"""

    optimal_rates = []
    optimal_count = 0

    for episode, action in enumerate(actions, start=1):
        if action == optimal_action:
            optimal_count += 1

        optimal_rates.append(optimal_count / episode)

    return optimal_rates


def run_experiment(env: Any, algorithm: Any, n_episodes: int) -> dict[str, list]:
    """Выполняет один эксперимент с выбранным алгоритмом"""

    rewards = []
    actions = []

    for episode in range(n_episodes):
        action = algorithm.select_action()

        reward = env.step(action)

        algorithm.update(action, reward)

        actions.append(action)
        rewards.append(reward)

    average_rewards = calculate_average_reward(rewards=rewards)
    optimal_action_rate = calculate_optimal_action_rate(actions=actions, optimal_action=env.optimal_action)

    return {
        "actions": actions,
        "rewards": rewards,
        "average_rewards": average_rewards,
        "optimal_action_rate": optimal_action_rate
    }


def run_multiple_experiments(env: Any, algorithm_factory: Any, n_episodes: int, n_runs: int) -> dict[str, list]:
    """Выполняет несколько независимых запусков эксперимента"""

    all_average_rewards = []
    all_optimal_action_rates = []

    for run in range(n_runs):
        algorithm = algorithm_factory()

        result = run_experiment(
            env=env,
            algorithm=algorithm,
            n_episodes=n_episodes
        )

        all_average_rewards.append(result ["average_rewards"])
        all_optimal_action_rates.append(result ["optimal_action_rate"])

    average_rewards = torch.tensor(all_average_rewards).mean(dim=0)
    optimal_action_rates = torch.tensor(all_optimal_action_rates).mean(dim=0)

    return {
        "average_rewards": average_rewards.tolist(),
        "optimal_action_rate": optimal_action_rates.tolist()
    }
