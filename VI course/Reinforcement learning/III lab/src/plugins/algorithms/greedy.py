import numpy as np

from src.plugins.monte_carlo_method.handler import MonteCarloHandler
from src.plugins.algorithms.base import Base
from src.config import START_STATES, MAX_STEPS


class GreedyHandler(Base):


    def action(self, q_values, state, rng):
        """Выбирает жадное действие для заданного состояния"""

        state_values = q_values[state]

        # Находим максимальное значение Q
        max_value = np.max(state_values)

        # Получаем индексы всех действий с максимальным Q
        best_actions = np.flatnonzero(state_values == max_value)

        # Случайно выбираем одно из лучших действий
        return int(rng.choice(best_actions))


    def generate_episode(self, env, q_values, rng, seed=None):
        """Генерирует эпизод с использованием Exploring Starts"""

        # Выбираем случайное начальное состояние
        initial_state = int(rng.choice(START_STATES))

        # Выбираем случайное начальное действие
        initial_action = int(rng.integers(env.n_actions))

        # Устанавливаем начальное состояние среды
        state = env.reset_to_state(
            state=initial_state,
            seed=seed,
        )

        episode = []

        # Первое действие задано Exploring Starts
        action = initial_action
        for _ in range(MAX_STEPS):

            next_state, reward, done, info = env.step(action)
            episode.append((state, action, reward))
            if done:
                break

            state = next_state

            # После первого шага используем жадную стратегию
            action = self.action(
                q_values=q_values,
                state=state,
                rng=rng,
            )

        return episode


    def train(self, env, n_episodes, gamma=1.0, seed=42):
        """Обучает жадную стратегию методом Monte-Carlo с использованием Exploring Starts"""

        rng = np.random.default_rng(seed)
        n_states = env.n_states
        n_actions = env.n_actions

        # Таблица ценности пар (состояние, действие)
        q_values = np.zeros((n_states, n_actions))

        # Сумма доходов для каждой пары
        returns_sum = np.zeros((n_states, n_actions))

        # Количество посещений каждой пары
        visits_count = np.zeros((n_states, n_actions))

        # Статистика успешных эпизодов
        episode_rewards = []
        for episode_idx in range(n_episodes):

            # Генерируем эпизод с Exploring Starts
            episode = self.generate_episode(
                env=env,
                q_values=q_values,
                rng=rng,
                seed=seed + episode_idx,
            )

            # Рассчитываем доходы для всех шагов
            returns = MonteCarloHandler.calculate_returns(
                episode=episode,
                gamma=gamma,
            )

            # Множество пар, уже встреченных в эпизоде
            visited_pairs = set()

            for (state, action, reward), total_return in zip(episode, returns):
                state_action = (state, action)

                # Используем First-Visit MC
                if state_action in visited_pairs:
                    continue

                visited_pairs.add(state_action)

                # Обновляем статистику
                returns_sum[state, action] += total_return
                visits_count[state, action] += 1

                # Обновляем среднюю оценку Q
                q_values[state, action] = (returns_sum[state, action]/ visits_count[state, action])

            # Сохраняем награду эпизода
            episode_rewards.append(sum(transition[2] for transition in episode))

        return q_values, visits_count, episode_rewards


    def evaluate(self, env, q_values, n_episodes=1000, seed=10000):
        """Оценивает обученную жадную стратегию"""

        rng = np.random.default_rng(seed)

        successful_episodes = 0
        total_steps = 0

        for episode_idx in range(n_episodes):
            state = env.reset(seed=seed + episode_idx)

            for step in range(1, MAX_STEPS + 1):
                action = self.action(
                    q_values=q_values,
                    state=state,
                    rng=rng,
                )

                next_state, reward, done, info = env.step(action)
                total_steps += 1
                state = next_state

                if done:
                    if reward > 0:
                        successful_episodes += 1
                    break

        success_rate = successful_episodes / n_episodes
        average_steps = total_steps / n_episodes

        return success_rate, average_steps
