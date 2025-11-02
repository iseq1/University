"""
Класс обработчик для получения расстояния Хэмминга
"""
from src.utils.vector_utils import get_hamming_distance
from src.models.boolean_function import BooleanFunction

class HammingService:

    @staticmethod
    def get_distance(f1: BooleanFunction, f2: BooleanFunction) -> int:
        """
        Расстояние Хэмминга между двумя булевыми функциями.
        """
        if f1.n != f2.n:
            raise ValueError("Функции должны быть одной размерности")
        return get_hamming_distance(f1.values, f2.values)