"""Файл, описывающий эксперименты над средой FrozenLake"""
from pathlib import Path
from typing import Any
import time

import pandas as pd
import gymnasium as gym

from plugins.algorithms import ValueIteration, PolicyIteration
from utils.plotting import plot_parameter_results


class Experiments:
    """Класс, описывающий все эксперименты над средой FrozenLake"""

    def __init__(self):
        self.env_configs = [
            ("4x4", True),
            ("4x4", False),
            ("8x8", True),
            ("8x8", False),
        ]
        self.algorithm_classes = {
            "Value Iteration": ValueIteration,
            "Policy Iteration": PolicyIteration,
        }
        self.base_params = {
            'gamma': 0.9,
            'theta': 1e-6,
        }


    @staticmethod
    def evaluate_policy(env: Any, policy: Any, n_episodes: int = 1000, seed: int = 42) -> dict:
        """
        Оценивает стратегию на случайных эпизодах
        :param env: Среда FrozenLake
        :param policy: Массив действий для каждого состояния
        :param n_episodes: Количество проверочных эпизодов
        :param seed: Начальное значение генератора случайных чисел
        :return: Словарь с результатами оценки
        """
        successes = 0
        total_steps = 0

        for episode in range(n_episodes):
            state, _ = env.reset(seed=seed if episode == 0 else None)

            for step in range(1, 1001):
                action = int(policy[state])

                state, reward, terminated, truncated, _ = env.step(action)

                if terminated or truncated:
                    successes += int(reward > 0)
                    total_steps += step
                    break
            else:
                # Эпизод не завершился за 1000 шагов.
                total_steps += 1000

        return {
            "episodes": n_episodes,
            "success_rate": successes / n_episodes,
            "successes": successes,
            "average_steps": total_steps / n_episodes,
        }


    def compare_algorithms(self, env: Any, gamma: float = None, theta: float = None, n_episodes: int = 1000) -> dict:
        """
        Сравнивает Value Iteration и Policy Iteration в одинаковой среде
        :param env: Среда FrozenLake.
        :param gamma: Коэффициент дисконтирования.
        :param theta: Порог сходимости.
        :param n_episodes: Количество эпизодов оценки стратегии.
        :return: Словарь с результатами сравнения.
        """
        if not gamma:
            gamma = self.base_params.get('gamma')

        if not theta:
            theta = self.base_params.get('theta')

        algorithms = {
            "Value Iteration": ValueIteration(
                env=env,
                gamma=gamma,
                theta=theta,
            ),
            "Policy Iteration": PolicyIteration(
                env=env,
                gamma=gamma,
                theta=theta,
            ),
        }

        results = {}

        for name, algorithm in algorithms.items():
            start_time = time.perf_counter()

            values, policy, history = algorithm.run()

            elapsed_time = time.perf_counter() - start_time

            evaluation = self.evaluate_policy(
                env=env,
                policy=policy,
                n_episodes=n_episodes,
                seed=42,
            )

            if name == "Value Iteration":
                iterations = len(history)
            else:
                iterations = algorithm.policy_iterations

            results[name] = {
                "values": values,
                "policy": policy,
                "iterations": iterations,
                "evaluation_sweeps": (
                    algorithm.evaluation_sweeps
                    if name == "Policy Iteration"
                    else None
                ),
                "time_seconds": elapsed_time,
                "success_rate": evaluation["success_rate"],
                "average_steps": evaluation["average_steps"],
            }

        return results


    def run_parameter_study_gamma(self, env: Any, n_episodes: int) -> list:
        """"Эксперимент влияния коэффициента дисконтирования"""

        experiments = []
        gamma_values = [0.5, 0.7, 0.9, 0.99]

        for algorithm_name, algorithm_class in self.algorithm_classes.items():
            for gamma in gamma_values:
                algorithm = algorithm_class(
                    env=env,
                    gamma=gamma,
                    theta=1e-6,
                )

                start_time = time.perf_counter()
                values, policy, history = algorithm.run()
                elapsed_time = time.perf_counter() - start_time

                evaluation = self.evaluate_policy(
                    env=env,
                    policy=policy,
                    n_episodes=n_episodes,
                    seed=42,
                )

                experiments.append({
                    "algorithm": algorithm_name,
                    "parameter": "gamma",
                    "parameter_value": gamma,
                    "iterations": (
                        len(history)
                        if algorithm_name == "Value Iteration"
                        else algorithm.policy_iterations
                    ),
                    "evaluation_sweeps": (
                        algorithm.evaluation_sweeps
                        if algorithm_name == "Policy Iteration"
                        else None
                    ),
                    "time_seconds": elapsed_time,
                    "success_rate": evaluation["success_rate"],
                    "average_steps": evaluation["average_steps"],
                })

        return experiments


    def run_parameter_study_theta(self, env: Any, n_episodes: int) -> list:
        """"Эксперимент влияния порога сходимости"""

        experiments = []
        theta_values = [1e-2, 1e-4, 1e-6, 1e-8]

        for algorithm_name, algorithm_class in self.algorithm_classes.items():
            for theta in theta_values:
                algorithm = algorithm_class(
                    env=env,
                    gamma=0.9,
                    theta=theta,
                )

                start_time = time.perf_counter()
                values, policy, history = algorithm.run()
                elapsed_time = time.perf_counter() - start_time

                evaluation = self.evaluate_policy(
                    env=env,
                    policy=policy,
                    n_episodes=n_episodes,
                    seed=42,
                )

                experiments.append({
                    "algorithm": algorithm_name,
                    "parameter": "theta",
                    "parameter_value": theta,
                    "iterations": (
                        len(history)
                        if algorithm_name == "Value Iteration"
                        else algorithm.policy_iterations
                    ),
                    "evaluation_sweeps": (
                        algorithm.evaluation_sweeps
                        if algorithm_name == "Policy Iteration"
                        else None
                    ),
                    "time_seconds": elapsed_time,
                    "success_rate": evaluation["success_rate"],
                    "average_steps": evaluation["average_steps"],
                })

        return experiments


    def run_parameter_study(self, env: Any, n_episodes: int = 500) -> pd.DataFrame:
        """
        Исследует влияние gamma и theta на работу алгоритмов.

        :param env: Среда FrozenLake.
        :param n_episodes: Количество эпизодов оценки стратегии.
        :return: Таблица результатов экспериментов.
        """

        return pd.DataFrame([
            *self.run_parameter_study_gamma(env=env, n_episodes=n_episodes),
            *self.run_parameter_study_theta(env=env, n_episodes=n_episodes)
        ])


    def run_environment_study(self, n_episodes: int = 1000) -> pd.DataFrame | None:
        """Эксперимент влияния конфигурации среды"""

        results = []

        for map_name, is_slippery in self.env_configs:
            env = gym.make(
                "FrozenLake-v1",
                map_name=map_name,
                is_slippery=is_slippery,
            )

            try:
                base_gamma, base_theta = self.base_params.values()

                for algorithm_name, algorithm_class in self.algorithm_classes.items():
                    algorithm = algorithm_class(
                        env=env,
                        gamma=base_gamma,
                        theta=base_theta,
                    )

                    start_time = time.perf_counter()
                    values, policy, history = algorithm.run()
                    elapsed_time = time.perf_counter() - start_time

                    evaluation = self.evaluate_policy(
                        env=env,
                        policy=policy,
                        n_episodes=n_episodes,
                        seed=42,
                    )

                    results.append({
                        "map": map_name,
                        "is_slippery": is_slippery,
                        "algorithm": algorithm_name,
                        "states": env.observation_space.n,
                        "iterations": (
                            len(history)
                            if algorithm_name == "Value Iteration"
                            else algorithm.policy_iterations
                        ),
                        "evaluation_sweeps": (
                            algorithm.evaluation_sweeps
                            if algorithm_name == "Policy Iteration"
                            else None
                        ),
                        "time_seconds": elapsed_time,
                        "success_rate": evaluation["success_rate"],
                        "average_steps": evaluation["average_steps"],
                    })
            finally:
                env.close()

        return pd.DataFrame(results)


    def handle(self, env):
        """Точка входа"""

        # 1.
        results = self.run_environment_study(n_episodes=1000)
        print(results.to_string(index=False))
        Path("results").mkdir(parents=True, exist_ok=True)
        results.to_csv("results/environment_study.csv", index=False)

        # 2.
        results = exp.run_parameter_study(env, n_episodes=500)
        print(results.to_string(index=False))
        results.to_csv("results/parameter_study.csv", index=False,)
        plot_parameter_results(results)


if __name__ == "__main__":
    exp = Experiments()
    results = exp.run_environment_study(n_episodes=1000)

    print(results.to_string(index=False))

    Path("results").mkdir(parents=True, exist_ok=True)
    results.to_csv("results/environment_study.csv", index=False)
