# src/models/boolean_function.py
from typing import Sequence, Tuple, List
from src.utils.vector_utils import get_all_inputs

class BooleanFunction:
    """
    Булева функция f: F2^n -> F2.
    values: список 0/1 длины 2^n, индекс соответствует бинарному представлению входа (MSB..LSB).
    """
    def __init__(self, n: int, values: Sequence[int]):
        if len(values) != 2 ** n:
            raise ValueError("Длина вектора значений должна быть равна 2^n")
        self.n = n
        # храним как список int 0/1
        self.values: List[int] = [int(v) & 1 for v in values]
        self.inputs: List[Tuple[int, ...]] = get_all_inputs(n)

    def value_at_index(self, idx: int) -> int:
        return int(self.values[idx])

    def value_at(self, x: Sequence[int]) -> int:
        # вычисляем индекс по битам MSB..LSB
        idx = 0
        for bit in x:
            idx = (idx << 1) | (int(bit) & 1)
        return int(self.values[idx])

    def __call__(self, x: Sequence[int]) -> int:
        return self.value_at(x)

    def __repr__(self):
        return f"BooleanFunction(n={self.n}, values={self.values})"
