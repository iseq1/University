"""Файл запуска"""

import gymnasium as gym

from utils import Experiments


env = gym.make(
    "FrozenLake-v1",
    map_name="4x4",
    is_slippery=True,
)



if __name__ == "__main__":

    try:
        Experiments().handle(env)
    finally:
        env.close()