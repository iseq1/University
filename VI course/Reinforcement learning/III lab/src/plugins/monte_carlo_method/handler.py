"""Метод Монте-Карло"""

import numpy as np

from src.plugins.monte_carlo_method.base import MonteCarloBase


class MonteCarloHandler(MonteCarloBase):
    """Основной обработчик метода Монте-Карло"""

    def __init__(self, env, n_episodes):
        self.env = env
        self.n_episodes = n_episodes
        self.seed = 42


    def prediction_first_visit(self, policy, gamma):
        """Оценка функции ценности методом First-Visit MC"""

        n_states = self.env.n_states

        # Сумма полученных доходов
        returns_sum = np.zeros(n_states)

        # Количество посещений состояний
        visits_count = np.zeros(n_states)

        rng = np.random.default_rng(self.seed)

        for episode_idx in range(self.n_episodes):

            # Генерируем эпизод
            episode = self.generate_episode(
                env=self.env,
                policy=policy,
                rng=rng,
                seed=self.seed + episode_idx,
            )

            # Рассчитываем доходы
            returns = self.calculate_returns(
                episode=episode,
                gamma=gamma
            )

            # Состояния, уже встречавшиеся в эпизоде
            visited_states = set()

            # Проходим эпизод от начала к концу
            for (state, action, reward), total_return in zip(episode, returns):

                if state in visited_states:
                    continue

                visited_states.add(state)

                returns_sum[state] += total_return
                visits_count[state] += 1

        # Рассчитываем среднее значение
        values = np.zeros(n_states)
        visited_mask = visits_count > 0
        values[visited_mask] = (returns_sum[visited_mask] / visits_count[visited_mask])

        return values, visits_count


    def prediction_every_visit(self, policy, gamma):
        """Оценка функции ценности методом Every-Visit MC"""

        n_states = self.env.n_states

        returns_sum = np.zeros(n_states)
        visits_count = np.zeros(n_states)

        rng = np.random.default_rng(self.seed)

        for episode_idx in range(self.n_episodes):

            episode = self.generate_episode(
                env=self.env,
                policy=policy,
                rng=rng,
                seed=self.seed + episode_idx,
            )

            returns = self.calculate_returns(
                episode=episode,
                gamma=gamma
            )

            # Учитываем каждое посещение состояния
            for (state, action, reward), total_return in zip(episode, returns):
                returns_sum[state] += total_return
                visits_count[state] += 1

        # Рассчитываем среднее значение
        values = np.zeros(n_states)
        visited_mask = visits_count > 0
        values[visited_mask] = (returns_sum[visited_mask] / visits_count[visited_mask])

        return values, visits_count


    def action_value_prediction(self, policy, gamma, first_visit=True):
        """Оценивает функцию ценности Q(s, a) для заданной стратегии"""

        n_states = self.env.n_states
        n_actions = self.env.n_actions

        # Сумма доходов для каждой пары (состояние, действие)
        returns_sum = np.zeros((n_states, n_actions))

        # Количество учтённых посещений каждой пары
        visits_count = np.zeros((n_states, n_actions))

        rng = np.random.default_rng(self.seed)

        for episode_idx in range(self.n_episodes):
            # Генерируем один эпизод
            episode = self.generate_episode(
                env=self.env,
                policy=policy,
                rng=rng,
                seed=self.seed + episode_idx,
            )

            # Рассчитываем доход для каждого шага
            returns = self.calculate_returns(
                episode=episode,
                gamma=gamma
            )

            # Множество уже учтённых пар в текущем эпизоде
            visited_pairs = set()

            for (state, action, reward), total_return in zip(episode, returns):
                state_action = (state, action)

                # Для First-Visit пропускаем повторные пары
                if first_visit and state_action in visited_pairs:
                    continue

                visited_pairs.add(state_action)

                # Накопление доходов и количества посещений
                returns_sum[state, action] += total_return
                visits_count[state, action] += 1

        # Рассчитываем средние значения Q(s, a)
        q_values = np.zeros((n_states, n_actions))
        visited_mask = visits_count > 0
        q_values[visited_mask] = (returns_sum[visited_mask] / visits_count[visited_mask])

        return q_values, visits_count
