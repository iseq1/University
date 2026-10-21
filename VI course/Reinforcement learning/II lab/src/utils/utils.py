"""Утилиты"""

ACTION_SYMBOLS = {
    0: "←",
    1: "↓",
    2: "→",
    3: "↑",
    -1: "·",
}


# Для отладки
def print_grid(values, shape=(4, 4), precision=4):
    """Выводит функцию ценности в виде матрицы"""
    grid = values.reshape(shape)

    for row in grid:
        print(
            " ".join(
                f"{value:{precision + 3}.{precision}f}"
                for value in row
            )
        )


# Для отладки
def print_policy(policy, shape=(4, 4)):
    """Выводит стратегию в виде стрелок"""
    grid = policy.reshape(shape)

    for row in grid:
        print(
            " ".join(
                f"  {ACTION_SYMBOLS[action]}  "
                for action in row
            )
        )