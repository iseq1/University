"""Общие настройки лабораторной работы"""

import numpy as np


# Параметры среды
ENV_NAME = "FrozenLake-v1"
MAP_NAME = "4x4"
IS_SLIPPERY = True

# Параметры экспериментов
GAMMA = 1.0
N_EPISODES = 100_000
N_EVALUATION_EPISODES = 100_000

# Воспроизводимость экспериментов
RANDOM_SEED = 42

# Максимальное количество шагов в одном эпизоде
MAX_STEPS = 500

# Все нетерминальные состояния FrozenLake 4x4.
START_STATES = np.array([
    0, 1, 2, 3,
    4, 6,
    8, 9, 10,
    13, 14,
])