"""
Файл содержит реализацию градиентного алгоритма для решения задачи об многоруком бандите
"""
from .base import BanditAlgorithmBase

import torch


class GradientAlgorithm(BanditAlgorithmBase):
    """Градиентный алгоритм решения задачи о многоруком бандите"""


    def __init__(self, n_actions: int, alpha: float = 0.1):
        """Инициализирует алгоритм и его внутреннее состояние"""

        if alpha <= 0:
            raise ValueError("Значение \"alpha\" должен быть положительным")

        super().__init__(n_actions)
        self.preferences = torch.zeros(n_actions) # Предпочтительности действий H(a)
        self.total_steps = 0 # Количество выполненных действий
        self.average_reward = 0.0 # Средняя награда
        self.alpha = alpha


    def select_action(self) -> int:
        """Выбирает действие на основе распределения вероятностей, полученного с помощью функции softmax"""

        # Преобразуем предпочтительности в вероятности
        probabilities = torch.softmax(
            self.preferences,
            dim=0
        )

        # Выбираем действие согласно распределению
        action = torch.multinomial(
            probabilities,
            num_samples=1
        ).item()

        return action


    def update(self, action: int, reward: float) -> None:
        """Обновляет предпочтительности действий после получения награды"""

        self.total_steps += 1

        # Обновляем среднюю награду
        self.average_reward += (
            reward - self.average_reward
        ) / self.total_steps

        # Вычисляем Softmax-вероятности
        probabilities = torch.softmax(
            self.preferences,
            dim=0
        )

        # Обновляем предпочтительности
        for current_action in range(self.n_actions):

            if current_action == action:
                self.preferences[current_action] += (
                    self.alpha
                    * (reward - self.average_reward)
                    * (1 - probabilities[current_action])
                )

            else:
                self.preferences[current_action] -= (
                    self.alpha
                    * (reward - self.average_reward)
                    * probabilities[current_action]
                )
