# src/models/sbox.py
from typing import Sequence, List
from src.models.boolean_function import BooleanFunction

class SBox:
    """
    s-box (n, m): отображение F2^n -> F2^m заданное таблицей длины 2^n,
    где каждый элемент — целое 0..2^m-1.
    """
    def __init__(self, n: int, m: int, table: Sequence[int]):
        if len(table) != 2 ** n:
            raise ValueError("Длина таблицы должна быть 2^n")
        self.n = n
        self.m = m
        self.table: List[int] = [int(v) for v in table]
        maxv = 2 ** m - 1
        for v in self.table:
            if v < 0 or v > maxv:
                raise ValueError("Значения таблицы должны быть в диапазоне [0, 2^m-1]")

        # построим m базовых булевых функций (бит i)
        self.basis: List[BooleanFunction] = []
        for bit in range(m):
            vals = [ (y >> bit) & 1 for y in self.table ]
            self.basis.append(BooleanFunction(n, vals))

    def is_permutation(self) -> bool:
        if self.n != self.m:
            return False
        return len(set(self.table)) == len(self.table)

    def has_fixed_points(self) -> bool:
        if not self.is_permutation():
            return False
        for i, v in enumerate(self.table):
            if v == i:
                return True
        return False

    def __repr__(self):
        return f"SBox(n={self.n}, m={self.m}, table_len={len(self.table)})"
