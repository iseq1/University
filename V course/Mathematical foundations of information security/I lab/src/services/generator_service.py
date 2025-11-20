"""
Сервис для генерации специальных булевых функций
"""
from src.models.bent_function import BentFunction


class GeneratorService:
    """
    Генератор булевых функций
    """

    @staticmethod
    def generate_bent(n: int) -> BentFunction:
        """
        Генерирует bent-функцию по стандартной конструкции: f(x1,...,xn) = x1*x2 ⊕ x3*x4 ⊕ ... ⊕ x_{n-1}*x_n

        :param n: число переменных
        :return: объект BentFunction с вектором значений и формулой
        """
        if n % 2 != 0:
            raise ValueError("Bent-функции существуют только для чётного n")

        values = []
        for i in range(2 ** n):
            x = tuple(map(int, f"{i:0{n}b}"))  # бинарное представление входа
            val = 0
            for j in range(0, n, 2):
                val ^= (x[j] & x[j + 1])  # XOR произведений соседних бит
            values.append(val)

        formula = " ⊕ ".join([f"x{j+1}x{j+2}" for j in range(0, n, 2)])

        return BentFunction(n, values, description=formula)
