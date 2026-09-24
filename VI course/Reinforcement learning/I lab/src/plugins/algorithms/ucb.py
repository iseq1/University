"""
Файл содержит реализацию алгоритма верхней доверительной границы для решения задачи об многоруком бандите
"""
from .base import BanditAlgorithmBase

import torch


class UCBAlgorithm(BanditAlgorithmBase):
    """Алгоритма верхней доверительной границы для решения задачи о многоруком бандите"""


    def __init__(self, n_actions: int, c: float = 1.0):
        """Инициализирует алгоритм и его внутреннее состояние"""

        if c < 0:
            raise ValueError("Значение \"C\" должен быть неотрицательным")

        super().__init__(n_actions)
        self.total_steps = 0
        self.c = c

    def select_action(self) -> int:
        """Выбирает действие с максимальным значением UCB"""

        # Сначала необходимо попробовать каждый рычаг хотя бы один раз
        for action in range(self.n_actions):
            if self.action_counts[action] == 0:
                return action

        ucb_values = []

        for action in range(self.n_actions):
            exploration_bonus = self.c * (
                torch.log(torch.tensor(float(self.total_steps)))
                / self.action_counts[action]
            ).sqrt()

            ucb_value = (
                self.action_values[action]
                + exploration_bonus.item()
            )

            ucb_values.append(ucb_value)

        return torch.argmax(
            torch.tensor(ucb_values)
        ).item()


    def update(self, action: int, reward: float) -> None:
        """Обновляет статистику выбранного действия"""
        self.total_steps += 1

        self.action_counts[action] += 1
        self.action_total_rewards[action] += reward

        self.action_values[action] = (self.action_total_rewards[action] / self.action_counts[action])
