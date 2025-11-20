"""
Представление булевой функции f: F2^n -> F2 через её вектор значений.

В теории булевых функций функция полностью задаётся таблицей истинности, содержащей 2^n значений — по одному для
каждого входного вектора x ∈ F2^n. Мы нумеруем входы в двоичном порядке (MSB..LSB), поэтому значение функции
f(x) хранится в массиве values по индексу, равному бинарному коду x.

Пример:
    n = 3
    values = [0,1,0,1,0,1,1,0]

    Тогда:
    f(000) = values[0] = 0
    f(001) = values[1] = 1
    f(010) = values[2] = 0
    ...
    f(111) = values[7] = 0

Этот объект является базой для расчёта нелинейности, расстояния Хэмминга
до линейных функций и других криптографических характеристик.
"""
from typing import Sequence, Tuple, List
from src.utils.vector_utils import get_all_inputs


class BooleanFunction:

    def __init__(self, n: int, values: Sequence[int]):
        """
        Создаёт булеву функцию по её вектору значений.

        :param n: число входных переменных (размерность F2^n)
        :param values: последовательность длины 2^n, содержащая 0/1 — значения функции
        :raises ValueError: если длина values не равна 2^n
        """
        if len(values) != 2 ** n:
            raise ValueError("Длина вектора значений должна быть равна 2^n")

        self.n = n
        self.values: List[int] = [(int(v) & 1) for v in values]
        self.inputs: List[Tuple[int, ...]] = get_all_inputs(n)


    def value_at_index(self, idx: int) -> int:
        """
        Возвращает значение функции по индексу таблицы.

        :param idx: индекс (0 ≤ idx < 2^n), соответствующий входу x.
        :return: 0 или 1
        """
        return int(self.values[idx])


    def value_at(self, x: Sequence[int]) -> int:
        """
        Возвращает значение функции f(x) по бинарному входу x.

        :param x: последовательность битов длины n (например, [1,0,1])
        :return: значение f(x) — 0 или 1
        """
        idx = 0
        for bit in x:
            idx = (idx << 1) | (int(bit) & 1)
        return int(self.values[idx])


    def __call__(self, x: Sequence[int]) -> int:
        return self.value_at(x)


    def __repr__(self):
        return f"BooleanFunction(n={self.n}, values={self.values})"
