"""
Класс обработчик нахождения степени нелинейности функции
"""
from itertools import product
from src.models.linear_function import BooleanFunction, LinearFunction
from src.services.hamming_service import HammingService

class NonlinearityService:

    @staticmethod
    def compute_nonlinearity(f: BooleanFunction) -> int | float:
        """
        Находит степень нелинейности функции f: минимальное расстояние до любой линейной (аффинной) функции.
        """
        n = f.n
        min_dist = float('inf')

        # Генерируем все возможные коэффициенты для линейных функций (a0...an)
        for coeffs in product([0, 1], repeat=n + 1):
            g = LinearFunction(n, list(coeffs))
            dist = HammingService.get_distance(f, g)
            if dist < min_dist:
                min_dist = dist

        return min_dist