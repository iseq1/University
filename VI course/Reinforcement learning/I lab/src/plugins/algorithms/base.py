"""
Файл содержит определение общего интерфейса алгоритмов для решения задачи об одноруком бандите
"""
from abc import ABC, abstractmethod


class BanditAlgorithmBase(ABC):
    """Базовый абстрактный класс для алгоритмов решения задачи о многоруком бандите"""

    def __init__(self, n_actions: int):
        """Инициализирует алгоритм и его внутреннее состояние"""
        self.n_actions = n_actions

        self.action_counts = [0] * n_actions
        self.action_total_rewards = [0] * n_actions
        self.action_values = [0.0] * n_actions


    @abstractmethod
    def select_action(self) -> int:
        """Выбирает действие для текущего шага взаимодействия со средой"""
        pass


    @abstractmethod
    def update(self, action: int, reward: float) -> None:
        """Обновляет внутреннее состояние алгоритма после получения награды"""
        pass