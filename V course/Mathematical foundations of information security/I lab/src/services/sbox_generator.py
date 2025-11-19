# src/services/sbox_generator.py
import random
from typing import List, Optional
from src.models.sbox import SBox
from src.services.sbox_nonlinearity_service import SBoxNonlinearityService

class SBoxGenerator:
    """
    Генератор s-box (в частности n=m=5). Стратегия:
    - случайная перестановка (перестановка 0..2^n-1),
    - удаление фиксированных точек (если требуется),
    - локальная оптимизация через случайные свапы (принимаем если NL не ухудшился).
    """
    def __init__(self, n: int = 5, m: Optional[int] = None, seed: Optional[int] = None):
        if m is None:
            m = n
        self.n = n
        self.m = m
        self.rng = random.Random(seed)

    def random_permutation(self) -> List[int]:
        size = 2 ** self.n
        perm = list(range(size))
        self.rng.shuffle(perm)
        return perm

    def fix_fixed_points(self, table: List[int]) -> List[int]:
        size = len(table)
        # простой метод: для каждого фиксированного i, ищем j != i и меняем
        for i in range(size):
            if table[i] == i:
                # ищем j с table[j] != j и table[j] != i
                for j in range(size):
                    if j != i and table[j] != j and table[j] != i:
                        table[i], table[j] = table[j], table[i]
                        break
        return table

    def search_best(self,
                    attempts: int = 10,
                    steps_per_attempt: int = 1000,
                    enforce_no_fixed_points: bool = True):
        best_tbl = None
        best_nl = None

        for attempt in range(attempts):
            table = self.random_permutation()
            if enforce_no_fixed_points:
                table = self.fix_fixed_points(table)
            sbox = SBox(self.n, self.m, table)
            current_nl = SBoxNonlinearityService.compute_sbox_nonlinearity(sbox)

            # локальная оптимизация: случайные свапы
            for _ in range(steps_per_attempt):
                i, j = self.rng.sample(range(len(table)), 2)
                # делаем свап
                table[i], table[j] = table[j], table[i]
                if enforce_no_fixed_points and (table[i] == i or table[j] == j):
                    # откат и пропуск
                    table[i], table[j] = table[j], table[i]
                    continue
                candidate = SBox(self.n, self.m, table)
                nl_candidate = SBoxNonlinearityService.compute_sbox_nonlinearity(candidate)
                # принимаем если не хуже
                if nl_candidate >= current_nl:
                    current_nl = nl_candidate
                    # оставляем swap
                else:
                    # откат
                    table[i], table[j] = table[j], table[i]

            # сохраняем лучший из попыток
            if best_tbl is None or current_nl > best_nl:
                best_tbl = table.copy()
                best_nl = current_nl

        if best_tbl is None:
            raise RuntimeError("Не удалось найти S-box (проверьте генератор).")
        return SBox(self.n, self.m, best_tbl), int(best_nl)
