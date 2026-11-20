import numpy as np

from src.plugins.algorithms.base import Base
from src.plugins.monte_carlo_method.handler import MonteCarloHandler
from src.config import MAX_STEPS, N_EPISODES, GAMMA, RANDOM_SEED, N_EVALUATION_EPISODES


class EpsilonGreedyHandler(Base):


    def action(self, q_values, state, epsilon, rng):
        """Выбирает действие по epsilon-жадной стратегии"""

        n_actions = q_values.shape[1]

        # Исследование: выбираем случайное действие
        if rng.random() < epsilon:
            return int(rng.integers(n_actions))

        # Использование знаний: выбираем лучшее действие
        state_values = q_values[state]
        best_value = np.max(state_values)

        # Если несколько действий имеют одинаковую оценку,
        # выбираем случайное среди них
        best_actions = np.flatnonzero(state_values == best_value)

        return int(rng.choice(best_actions))


    def generate_episode(self, env, q_values, epsilon, rng, seed=None):
        """Генерирует эпизод, используя epsilon-жадную стратегию"""

        state = env.reset(seed=seed)
        episode = []

        for _ in range(MAX_STEPS):
            action = self.action(
                q_values=q_values,
                state=state,
                epsilon=epsilon,
                rng=rng,
            )

            next_state, reward, done, _ = env.step(action)
            episode.append((state, action, reward))
            state = next_state

            if done:
                break

        return episode


    def train(self, env, epsilon=0.1, n_episodes=N_EPISODES, gamma=GAMMA, seed=RANDOM_SEED):
        """Обучает epsilon-жадную стратегию методом Monte Carlo"""

        if not 0.0 <= epsilon <= 1.0:
            raise ValueError(
                "epsilon должен находиться в диапазоне [0, 1]"
            )

        rng = np.random.default_rng(seed)

        n_states = env.n_states
        n_actions = env.n_actions

        # Оценки качества действий
        q_values = np.zeros((n_states, n_actions))

        # Сумма возвратов для каждой пары (state, action)
        returns_sum = np.zeros((n_states, n_actions))

        # Количество посещений каждой пары
        visits_count = np.zeros((n_states, n_actions), dtype=int)

        # Награда, полученная в каждом эпизоде
        episode_rewards = []

        for episode_idx in range(n_episodes):
            episode = self.generate_episode(
                env=env,
                q_values=q_values,
                epsilon=epsilon,
                rng=rng,
                seed=seed + episode_idx,
            )

            returns = MonteCarloHandler.calculate_returns(
                episode=episode,
                gamma=gamma
            )

            visited_pairs = set()

            # First-Visit Monte Carlo
            for (state, action, reward), G in zip(episode, returns):
                pair = (state, action)

                # Обрабатываем только первое посещение пары
                if pair in visited_pairs:
                    continue

                visited_pairs.add(pair)

                returns_sum[state, action] += G
                visits_count[state, action] += 1

                # Обновляем среднюю оценку Q(s, a)
                q_values[state, action] = (returns_sum[state, action] / visits_count[state, action])

            # Сохраняем суммарную награду эпизода
            total_reward = sum(step[2] for step in episode)
            episode_rewards.append(total_reward)

        return q_values, visits_count, episode_rewards


    def evaluate(self, env, q_values, n_episodes=N_EVALUATION_EPISODES, seed=RANDOM_SEED + 100_000):
        """Оценивает жадную политику, полученную из Q-таблицы"""
        rng = np.random.default_rng(seed)

        successful_episodes = 0
        total_steps = 0

        for episode_idx in range(n_episodes):
            state = env.reset(seed=seed + episode_idx)

            for step in range(1, MAX_STEPS + 1):
                action = self.action(
                    q_values=q_values,
                    state=state,
                    epsilon=0.0,
                    rng=rng,
                )

                next_state, reward, done, _ = env.step(action)
                total_steps += 1
                state = next_state

                if done:
                    if reward > 0:
                        successful_episodes += 1
                    break

        success_rate = successful_episodes / n_episodes
        average_steps = total_steps / n_episodes

        return success_rate, average_steps
