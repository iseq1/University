"""Файл, описывающий алгоритм итерации по стратегиям"""
from typing import Any

import numpy as np

from base import Base


class PolicyIteration(Base):
    """Алгоритм итерации по стратегиям для FrozenLake"""

    def __init__(
        self,
        env: Any,
        gamma: float = 0.9,
        theta: float = 1e-6,
        max_iterations: int = 100_000,
    ):
        """
        Инициализирует алгоритм
        :param env: Среда с моделью переходов P
        :param gamma: Коэффициент дисконтирования
        :param theta: Порог сходимости оценки стратегии
        :param max_iterations: Максимальное число итераций
        """
        super().__init__(env, gamma, theta, max_iterations)

        # Счётчики для анализа алгоритма
        self.policy_iterations = 0 # количество внешних итераций, в которых выполняются оценка и улучшение стратегии
        self.evaluation_sweeps = 0 # общее количество проходов по всем состояниям при оценке стратегии


    def evaluate_policy(self, policy, values, history: list):
        """Оценивает текущую стратегию итерационным методом"""

        for _ in range(self.max_iterations):
            new_values = values.copy()

            for state in range(self.n_states):
                if state in self.terminal_states:
                    new_values[state] = 0.0
                    continue

                # Получаем оценку действия, предписанного стратегией
                action = policy[state]
                new_values[state] = self.calculate_action_value(
                    state=state,
                    action=action,
                    values=values,
                )

            delta = np.max(np.abs(new_values - values))

            values = new_values
            history.append(delta)
            self.evaluation_sweeps += 1

            if delta < self.theta:
                return values

        raise RuntimeError(
            "Оценка стратегии не достигла сходимости."
        )


    def improve_policy(self, policy, values):
        """Улучшает стратегию на основе функции ценности"""

        policy_stable = True

        for state in range(self.n_states):
            if state in self.terminal_states:
                continue

            old_action = policy[state]

            action_values = [
                self.calculate_action_value(
                    state=state,
                    action=action,
                    values=values,
                )
                for action in range(self.n_actions)
            ]

            best_action = int(np.argmax(action_values))
            policy[state] = best_action

            if best_action != old_action:
                policy_stable = False

        return policy_stable


    def run(self):
        """Выполняет итерацию по стратегиям"""

        values = np.zeros(self.n_states)

        # Начальная стратегия: действие 0 во всех состояниях.
        policy = np.zeros(self.n_states, dtype=int)

        for state in self.terminal_states:
            policy[state] = -1

        history = []

        for iteration in range(1, self.max_iterations + 1):
            # Оцениваем текущую стратегию
            values = self.evaluate_policy(
                policy=policy,
                values=values,
                history=history,
            )

            # Улучшаем стратегию
            policy_stable = self.improve_policy(
                policy=policy,
                values=values,
            )

            self.policy_iterations = iteration

            if policy_stable:
                return values, policy, history

        raise RuntimeError(
            f"Policy Iteration не завершился за {self.max_iterations} итераций."
        )


if __name__ == "__main__":
    import gymnasium as gym

    PolicyIteration(
        env=gym.make(
            "FrozenLake-v1",
            map_name="4x4",
            is_slippery=True,
        )
    ).run()