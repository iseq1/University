"""
Файл описывающий среду для моделирования задачи о многоруком бандите
"""
import torch


class BanditEnv:
    """Среда для моделирования задачи о многоруком бандите"""

    CONFIG = {
        3: {
            "payout": [0.10, 0.15, 0.30],
            "reward": [4, 3, 1]
        },

        5: {
            "payout": [0.10, 0.15, 0.30, 0.20, 0.25],
            "reward": [4, 3, 1, 1, 1]
        },

        10: {
            "payout": [
                0.10, 0.15, 0.30, 0.20, 0.25, 0.20, 0.10, 0.15, 0.20, 0.10
            ],
            "reward": [
                4, 3, 1, 1, 1, 1, 2, 1, 1, 2
            ]
        },

        20: {
            "payout": [
                0.10, 0.15, 0.30, 0.20, 0.25, 0.20, 0.10, 0.15, 0.20, 0.10,
                0.20, 0.10, 0.15, 0.20, 0.10, 0.15, 0.20, 0.10, 0.15, 0.20
            ],
            "reward": [
                4, 3, 1, 1, 1, 1, 2, 1, 1, 2,
                1, 2, 1, 1, 2, 1, 1, 2, 1, 1
            ]
        }
    }

    def __init__(self, payout_list: list[float] = None, reward_list: list[float] = None, n_lever: int = 3):
        """Инициализирует среду многорукого бандита"""

        if not payout_list and not reward_list:
            config= self.CONFIG.get(n_lever, {})
            payout_list = config.get("payout", [])
            reward_list = config.get("reward", [])

        if len(payout_list) != len(reward_list):
            raise ValueError(
                "Количество вероятностей и наград должно совпадать"
            )

        if not all(0 <= p <= 1 for p in payout_list):
            raise ValueError(
                "Вероятности должны находиться в диапазоне [0, 1]"
            )

        self.payout_list = payout_list
        self.reward_list = reward_list
        self.n_actions = len(payout_list)


    def step(self, action: int) -> float:
        """Выполняет выбранное действие и возвращает полученную награду"""

        if not 0 <= action < self.n_actions:
            raise ValueError(
                f"Некорректное действие: {action}"
            )

        if torch.rand(1).item() < self.payout_list[action]:
            return self.reward_list[action]

        return 0


    @property
    def expected_rewards(self) -> list[float]:
        """Возвращает математическое ожидание награды для каждого рычага"""
        return [
            p * r
            for p, r in zip(self.payout_list, self.reward_list)
        ]


    @property
    def optimal_action(self) -> int:
        """Возвращает индекс оптимального рычага"""

        return max(
            range(self.n_actions),
            key=lambda action: self.expected_rewards[action]
        )
