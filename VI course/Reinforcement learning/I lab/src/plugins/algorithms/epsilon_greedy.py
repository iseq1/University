"""
Файл содержит реализацию эпсилон-жадного алгоритма для решения задачи об многоруком бандите
"""
from .base import BanditAlgorithmBase

import torch


class EpsilonGreedyAlgorithm(BanditAlgorithmBase):
    """Эпсилон-жадный алгоритм решения задачи о многоруком бандите"""


    def __init__(self, n_actions: int, epsilon: float = 0.5):
        """Инициализирует алгоритм и его внутреннее состояние"""

        if not 0 <= epsilon <= 1:
            raise ValueError("epsilon должен находиться в диапазоне [0, 1]")

        super().__init__(n_actions)
        self.epsilon = epsilon


    def select_action(self) -> int:
        """Выбирает действие согласно эпсилон-жадный стратегии"""

        # С вероятностью epsilon исследуем случайный рычаг
        if torch.rand(1).item() < self.epsilon:
            return torch.randint(
                low=0,
                high=self.n_actions,
                size=(1,)
            ).item()

        # Иначе используем лучший найденный рычаг
        return torch.argmax(
            torch.tensor(self.action_values)
        ).item()


    def update(self, action: int, reward: float) -> None:
        """Обновляет статистику выбранного действия"""

        self.action_counts[action] += 1
        self.action_total_rewards[action] += reward

        self.action_values[action] = (self.action_total_rewards[action] / self.action_counts[action])
