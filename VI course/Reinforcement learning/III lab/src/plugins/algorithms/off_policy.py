import numpy as np

from src.plugins.algorithms.base import Base
from src.config import MAX_STEPS, N_EVALUATION_EPISODES, RANDOM_SEED


class OffPolicyHandler(Base):
    """Off-policy Monte Carlo Control с Weighted Importance Sampling

    Behavior policy: равномерное распределение действий
    Target policy: детерминированная жадная стратегия
    """

    @staticmethod
    def target_action(q_values, state):
        """Возвращает действие целевой детерминированной greedy-политики

        При равных Q-значениях выбирается действие с наименьшим индексом
        Это обеспечивает однозначность target policy для importance sampling
        """
        return int(np.argmax(q_values[state]))

    def action(self, q_values, state, rng):
        """Действие behavior policy: равномерный случайный выбор."""
        return int(rng.integers(q_values.shape[1]))

    def generate_episode(self, env, rng, seed=None):
        """Генерирует эпизод по равномерной behavior policy."""
        state = env.reset(seed=seed)
        episode = []

        for _ in range(MAX_STEPS):
            action = int(rng.integers(env.n_actions))
            next_state, reward, done, _ = env.step(action)
            episode.append((state, action, reward))
            state = next_state
            if done:
                break

        return episode

    def train(
        self,
        env,
        n_episodes,
        gamma=1.0,
        seed=RANDOM_SEED,
    ):
        """Обучает Q(s,a) методом off-policy MC с взвешенным IS

        Обновление выполняется в обратном порядке по эпизоду:
            C(s,a) <- C(s,a) + W
            Q(s,a) <- Q(s,a) + W/C(s,a) * (G - Q(s,a))

        Для равномерной behavior policy вероятность действия равна 1/A,
        поэтому отношение importance sampling на каждом согласованном
        шаге умножает вес на A
        """
        if n_episodes <= 0:
            raise ValueError("n_episodes должен быть положительным")
        if not 0.0 <= gamma <= 1.0:
            raise ValueError("gamma должен находиться в диапазоне [0, 1]")

        rng = np.random.default_rng(seed)
        q_values = np.zeros((env.n_states, env.n_actions), dtype=np.float64)
        cumulative_weights = np.zeros_like(q_values)
        visits_count = np.zeros_like(q_values, dtype=np.int64)
        episode_rewards = []

        n_actions = env.n_actions
        behavior_probability = 1.0 / n_actions

        for episode_idx in range(n_episodes):
            episode = self.generate_episode(
                env=env,
                rng=rng,
                seed=seed + episode_idx,
            )
            episode_rewards.append(float(sum(step[2] for step in episode)))

            G = 0.0
            W = 1.0

            for state, action, reward in reversed(episode):
                G = float(reward) + gamma * G

                cumulative_weights[state, action] += W
                visits_count[state, action] += 1

                q_values[state, action] += (
                    W / cumulative_weights[state, action]
                ) * (G - q_values[state, action])

                # Если действие behavior policy не совпало с действием
                # target policy, дальнейшие префиксы не имеют веса
                if action != self.target_action(q_values, state):
                    break

                W /= behavior_probability

        return q_values, visits_count, episode_rewards

    def evaluate(
        self,
        env,
        q_values,
        n_episodes=N_EVALUATION_EPISODES,
        seed=RANDOM_SEED + 100_000,
    ):
        """Оценивает детерминированную target policy без исследования."""
        successful_episodes = 0
        total_steps = 0

        for episode_idx in range(n_episodes):
            state = env.reset(seed=seed + episode_idx)

            for step in range(1, MAX_STEPS + 1):
                action = self.target_action(q_values, state)
                state, reward, done, _ = env.step(action)
                total_steps += 1

                if done:
                    if reward > 0:
                        successful_episodes += 1
                    break

        return successful_episodes / n_episodes, total_steps / n_episodes
