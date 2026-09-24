"""
Файл содержит реализацию жадного алгоритма для решения задачи об многоруком бандите
"""
import torch

from .base import BanditAlgorithmBase


class GreedyAlgorithm(BanditAlgorithmBase):
    """Жадный алгоритм решения задачи о многоруком бандите"""


    def __init__(self, n_actions: int, empty_param: None = None):
        """Инициализирует алгоритм и его внутреннее состояние"""
        super().__init__(n_actions=n_actions)


    def select_action(self) -> int:
        """Выбирает действие согласно жадной стратегии"""

        # Сначала пробуем каждый рычаг хотя бы один раз
        for action in range(self.n_actions):
            if self.action_counts[action] == 0:
                return action

        # После первоначального исследования всегда выбираем рычаг с максимальной оценкой
        return torch.argmax(
            torch.tensor(self.action_values)
        ).item()


    def update(self, action: int, reward: float) -> None:
        """Обновляет статистику выбранного действия"""
        self.action_counts[action] += 1
        self.action_total_rewards[action] += reward

        self.action_values[action] = (self.action_total_rewards[action] / self.action_counts[action])
