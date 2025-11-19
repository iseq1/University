# src/services/nonlinearity_service.py
from itertools import product
from src.models.linear_function import LinearFunction
from src.models.boolean_function import BooleanFunction
from src.services.hamming_service import HammingService

class NonlinearityService:
    """
    Нелинейность вычисляется как min_{g in LF_n} ρ(f, g),
    т.е. перебором всех линейных (аффинных) функций.
    """
    @staticmethod
    def compute_nonlinearity(f: BooleanFunction) -> int:
        n = f.n
        min_dist = None
        # перебираем все коэффициенты a0..an
        for coeffs in product([0, 1], repeat=n + 1):
            g = LinearFunction(n, list(coeffs))
            dist = HammingService.get_distance(f, g)
            if min_dist is None or dist < min_dist:
                min_dist = dist
                # оптимизация: если min_dist == 0 — дальше некуда
                if min_dist == 0:
                    return 0
        return int(min_dist if min_dist is not None else 0)
