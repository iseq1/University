from typing import Any
from abc import ABC, abstractmethod

import numpy as np


class Base(ABC):
    """Базовый абстрактный класс алгоритмов"""


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


    @abstractmethod
    def run(self): pass


    def calculate_action_value(self, state: int, action: int, values: np.ndarray) -> float:
        """Вычисляет ожидаемую ценность действия"""
        action_value = 0.0

        # Все возможные исходы выполнения действия a из клетки s
        transitions = self.env.unwrapped.P[state][action]

        # Расчёт будущей ценности
        for probability, next_state, reward, terminated in transitions:
            # Если эпизод завершен - будущая ценность равна 0, иначе - берем текущую оценку V(s')
            future_value = self.gamma * values[next_state] if not terminated else 0.0

            action_value += probability * (reward + future_value)

        return action_value
