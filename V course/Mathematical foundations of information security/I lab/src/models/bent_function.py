"""
Класс для представления bent-функций — максимально нелинейных булевых функций.
"""
from src.models.boolean_function import BooleanFunction


class BentFunction(BooleanFunction):
    """
    Класс для представления bent-функции.
    """

    def __init__(self, n: int, values, description: str = ""):
        """
        :param n: число переменных
        :param values: таблица истинности функции длины 2^n
        :param description: текстовое описание, например "x1*x2 ⊕ x3*x4"
        """
        super().__init__(n, values)
        self.description = description

    def __repr__(self):
        desc = f", desc='{self.description}'" if self.description else ""
        return f"BentFunction(n={self.n}{desc})"
