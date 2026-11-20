"""Модуль для работы с окружающей средой FrozenLake"""

import gymnasium as gym

from src.config import ENV_NAME, MAP_NAME, IS_SLIPPERY


class FrozenLakeEnvironment:
    """Обертка над средой FrozenLake"""

    def __init__(self, render_mode=None):
        """Инициализация окружающей среды"""

        self.env = gym.make(
            ENV_NAME,
            map_name=MAP_NAME,
            is_slippery=IS_SLIPPERY,
            render_mode=render_mode,
        )

        self.n_states = self.env.observation_space.n
        self.n_actions = self.env.action_space.n


    def reset(self, seed: int | None = None):
        """Сброс среды и получение начального состояния"""
        state, info = self.env.reset(seed=seed)
        return state


    def reset_to_state(self, state, seed=None):
        """Сбрасывает среду и устанавливает заданное начальное состояние. Используется для реализации Exploring Starts"""
        self.env.reset(seed=seed)
        self.env.unwrapped.s = int(state)
        return int(state)


    def step(self, action):
        """Выполнение действия и получение результата"""

        state, reward, terminated, truncated, info = (
            self.env.step(action)
        )

        done = terminated or truncated

        return state, reward, done, info


    def sample_action(self):
        """Получение случайного действия"""
        return self.env.action_space.sample()


    def render(self):
        """Отображение текущего состояния среды"""
        return self.env.render()


    def close(self):
        """Освобождение ресурсов среды"""
        self.env.close()
