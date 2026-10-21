"""Файл, описывающий алгоритм итерации по стратегиям"""
from typing import Any

import numpy as np


class PolicyIteration:
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

        if not 0 <= gamma < 1:
            raise ValueError("gamma должен находиться в диапазоне [0, 1).")

        if theta <= 0:
            raise ValueError("theta должен быть больше нуля.")

        if max_iterations <= 0:
            raise ValueError("max_iterations должен быть больше нуля.")

        self.env = env
        self.gamma = gamma
        self.theta = theta
        self.max_iterations = max_iterations

        self.n_states = env.observation_space.n
        self.n_actions = env.action_space.n

        description = env.unwrapped.desc.flatten()
        self.terminal_states = {
            state
            for state, cell in enumerate(description)
            if cell in (b"H", b"G")
        }

        # Счётчики для анализа алгоритма.
        self.policy_iterations = 0
        self.evaluation_sweeps = 0


    def calculate_action_value(self, state, action, values) -> float:
        """Вычисляет ожидаемую ценность действия"""
        action_value = 0.0

        transitions = self.env.unwrapped.P[state][action]

        for probability, next_state, reward, terminated in transitions:
            future_value = 0.0

            if not terminated:
                future_value = self.gamma * values[next_state]

            action_value += probability * (
                reward + future_value
            )

        return action_value


    def evaluate_policy(self, policy, values, history):
        """Оценивает текущую стратегию итерационным методом"""

        for _ in range(self.max_iterations):
            new_values = values.copy()

            for state in range(self.n_states):
                if state in self.terminal_states:
                    new_values[state] = 0.0
                    continue

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
            # Шаг 1. Оцениваем текущую стратегию.
            values = self.evaluate_policy(
                policy=policy,
                values=values,
                history=history,
            )

            # Шаг 2. Улучшаем стратегию.
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
