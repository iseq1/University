"""
Сервис для вычисления нелинейности булевой функции.
"""

from itertools import product
from src.models.linear_function import LinearFunction
from src.models.boolean_function import BooleanFunction
from src.services.hamming_service import HammingService


class NonlinearityService:
    """
    Класс, вычисляющий нелинейность булевой функции.
    """

    @staticmethod
    def compute_nonlinearity(f: BooleanFunction) -> int:
        """
        Перебирает все аффинные функции и находит минимальное расстояние Хэмминга.

        :param f: булева функция, для которой вычисляется нелинейность
        :return: нелинейность f
        """
        n = f.n
        min_dist = None

        # Перебор всех 2^(n+1) наборов коэффициентов
        for coeffs in product([0, 1], repeat=n + 1):
            g = LinearFunction(n, list(coeffs))  # создаём аффинную функцию
            dist = HammingService.get_distance(f, g)

            if min_dist is None or dist < min_dist:
                min_dist = dist

                # если нашли 0 — это минимум возможного
                if min_dist == 0:
                    return 0

        return int(min_dist if min_dist is not None else 0)
