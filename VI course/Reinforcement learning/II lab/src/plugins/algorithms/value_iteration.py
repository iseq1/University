"""Файл, описывающий алгоритм итерации по ценности"""
from typing import Any

import numpy as np


class ValueIteration:
    """Алгоритм итерации по ценности для среды FrozenLake"""

    def __init__(
        self,
        env: Any,
        gamma: float = 0.9,
        theta: float = 1e-6,
        max_iterations: int = 100_000,
    ):
        """
        Инициализация алгоритма
        :param env: Среда с доступной моделью переходов P
        :param gamma: Коэффициент дисконтирования
        :param theta: Порог сходимости
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

        # Состояния, соответствующие прорубям и цели.
        description = env.unwrapped.desc.flatten()
        self.terminal_states = {
            state
            for state, cell in enumerate(description)
            if cell in (b"H", b"G")
        }


    def calculate_action_value(self, state, action, values) -> float:
        """Вычисляет ожидаемую ценность действия."""
        action_value = 0.0

        transitions = self.env.unwrapped.P[state][action]

        # Суммирование по всем возможным исходам перехода (вероятность * ценность исхода)
        for probability, next_state, reward, terminated in transitions:

            # Если эпизод завершен, будущая ценность равна 0, иначе берем текущую оценку V(s')
            future_value = 0.0
            if not terminated:
                future_value = self.gamma * values[next_state]

            action_value += probability * (
                reward + future_value
            )

        return action_value


    def run(self) -> tuple:
        """Выполнение итерации по ценности"""
        values = np.zeros(self.n_states)
        history = []

        for iteration in range(1, self.max_iterations + 1):
            new_values = values.copy()

            for state in range(self.n_states):

                # Терминальные состояния всегда имеют ценность 0 (конец эпизода)
                if state in self.terminal_states:
                    new_values[state] = 0.0
                    continue

                # Перебор всех действий для поиска оптимального (принцип максимизации Беллмана)
                action_values = [
                    self.calculate_action_value(
                        state=state,
                        action=action,
                        values=values,
                    )
                    for action in range(self.n_actions)
                ]

                # Обновляем ценность состояния максимумом среди всех действий (оптимальная стратегия)
                new_values[state] = max(action_values)

            # Вычисляем меру сходимости (максимальное изменение за итерацию)
            delta = np.max(np.abs(new_values - values))
            history.append(delta)

            values = new_values

            # Критерий остановки: если изменения стали пренебрежимо малы, решение сошлось
            if delta < self.theta:
                break

        else:
            raise RuntimeError(
                "Алгоритм не достиг сходимости за "
                f"{self.max_iterations} итераций."
            )

        # Извлекаем стратегию из итоговой функции ценности.
        policy = np.full(self.n_states, -1, dtype=int)

        for state in range(self.n_states):
            if state in self.terminal_states:
                continue

            action_values = [
                self.calculate_action_value(
                    state=state,
                    action=action,
                    values=values,
                )
                for action in range(self.n_actions)
            ]

            policy[state] = int(np.argmax(action_values))

        return values, policy, history
