"""
Класс, представляющий S-box — нелинейное отображение F2^n → F2^m
"""

from typing import Sequence, List
from src.models.boolean_function import BooleanFunction


class SBox:
    """
    Класс SBox представляет таблицу замен F2^n → F2^m.
    """

    def __init__(self, n: int, m: int, table: Sequence[int]):
        """
        :param n: число входных бит
        :param m: число выходных бит
        :param table: последовательность целых значений от 0 до 2^m − 1 длины 2^n
        """
        if len(table) != 2 ** n:
            raise ValueError("Длина таблицы должна быть 2^n")

        self.n = n
        self.m = m
        self.table: List[int] = [int(v) for v in table]

        maxv = 2 ** m - 1
        for v in self.table:
            if not (0 <= v <= maxv):
                raise ValueError("Значения таблицы должны быть в диапазоне [0 .. 2^m - 1]")

        # Строим список компонентных булевых функций (m штук)
        self.basis: List[BooleanFunction] = []
        for bit in range(m):
            # Берём бит bit из каждого результата
            vals = [(y >> bit) & 1 for y in self.table]
            self.basis.append(BooleanFunction(n, vals))


    def is_permutation(self) -> bool:
        """
        Проверяет, является ли S-box перестановкой.

        :return: True, если S — биекция F2^n → F2^n.
        """
        if self.n != self.m:
            return False
        return len(set(self.table)) == len(self.table)


    def has_fixed_points(self) -> bool:
        """
        Проверяет, есть ли x такое, что S(x) = x.

        :return: True, если существует x: S(x) = x.
        """
        if not self.is_permutation():
            return False

        for i, v in enumerate(self.table):
            if v == i:
                return True
        return False


    def __repr__(self):
        return f"SBox(n={self.n}, m={self.m}, table_len={len(self.table)})"
