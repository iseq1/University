"""Файл, описывающий алгоритм итерации по ценности"""
from typing import Any

import numpy as np

from base import Base


class ValueIteration(Base):
    """Алгоритм итерации по ценности для среды FrozenLake"""

    def __init__(
        self,
        env: Any,
        gamma: float = 0.9,
        theta: float = 1e-6,
        max_iterations: int = 100_000
    ):
        """
        Инициализация алгоритма
        :param env: Среда с доступной моделью переходов P
        :param gamma: Коэффициент дисконтирования
        :param theta: Порог сходимости
        :param max_iterations: Максимальное число итераций
        """
        super().__init__(env, gamma, theta, max_iterations)


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

                # Перебор всех действий из A для поиска оптимального
                action_values = [
                    self.calculate_action_value(
                        state=state,
                        action=action,
                        values=values,
                    )
                    for action in range(self.n_actions)
                ]

                # Берем действие с максимальной ценностью (оптимальная стратегия)
                new_values[state] = max(action_values)

            # Вычисляем меру сходимости (максимальное изменение за итерацию) и фиксируем историю
            delta = np.max(np.abs(new_values - values))
            history.append(delta)

            values = new_values

            # Критерий остановки: если изменения стали очень малы, решение сошлось
            if delta < self.theta:
                break

        else:
            raise RuntimeError(
                "Алгоритм не достиг сходимости за "
                f"{self.max_iterations} итераций."
            )

        # Извлекаем стратегию из итоговой функции ценности
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


if __name__ == "__main__":
    import gymnasium as gym


    ValueIteration(
        env=gym.make(
            "FrozenLake-v1",
            map_name="4x4",
            is_slippery=True,
        )
    ).run()