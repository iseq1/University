"""
Класс представление булевой функции
"""
from src.utils.vector_utils import get_all_inputs

class BooleanFunction:
    """
    Класс представляет булеву функцию f: F2^n -> F2.
    """

    def __init__(self, n: int, values: list[int]):
        if len(values) != 2 ** n:
            raise ValueError("Длина вектора значений должна быть равна 2^n")
        self.n = n
        self.values = values
        self.inputs = get_all_inputs(n)

    def __call__(self, x: tuple[int]) -> int:
        """Позволяет вызывать объект как функцию."""
        idx = int("".join(map(str, x)), 2)
        return self.values[idx]

    def __repr__(self):
        return f"BooleanFunction(n={self.n}, values={self.values})"