# src/services/generator_service.py
from src.models.bent_function import BentFunction

class GeneratorService:
    """
    Генераторы специальных булевых функций.
    """
    @staticmethod
    def generate_bent(n: int) -> BentFunction:
        """
        Стандартный конструктор bent-функции:
        f = x1*x2 ⊕ x3*x4 ⊕ ... (работает для чётных n)
        """
        if n % 2 != 0:
            raise ValueError("Bent-функции существуют только для чётного n")

        values = []
        for i in range(2 ** n):
            x = tuple(map(int, f"{i:0{n}b}"))  # MSB..LSB
            val = 0
            for j in range(0, n, 2):
                val ^= (x[j] & x[j + 1])
            values.append(val)

        formula = " ⊕ ".join([f"x{j+1}x{j+2}" for j in range(0, n, 2)])
        return BentFunction(n, values, description=formula)
