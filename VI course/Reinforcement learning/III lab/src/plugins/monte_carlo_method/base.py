import numpy as np

from src.config import MAX_STEPS


class MonteCarloBase:
    """Базовый класс описывающий метод Монте-Карло"""

    @staticmethod
    def generate_episode(env, policy, rng=None, seed=None):
        """Генерирует один эпизод взаимодействия агента со средой"""

        if rng is None:
            rng = np.random.default_rng()

        state = env.reset(seed=seed)

        episode = []

        for _ in range(MAX_STEPS):
            # Выбор действия согласно стратегии
            action = policy(state, rng)

            # Выполнение действия
            next_state, reward, done, info = env.step(action)

            # Сохранение перехода
            episode.append((state, action, reward))

            state = next_state

            if done:
                break

        return episode


    @staticmethod
    def random_policy(state, rng):
        """Случайная стратегия выбора действий"""
        return int(rng.integers(0, 4))


    @staticmethod
    def calculate_returns(episode, gamma):
        """Рассчитывает доход для каждого шага эпизода"""

        returns = [0.0] * len(episode)

        total_return = 0.0

        # Проходим эпизод в обратном порядке
        for t in reversed(range(len(episode))):
            state, action, reward = episode[t]

            total_return = reward + gamma * total_return

            returns[t] = total_return

        return returns
