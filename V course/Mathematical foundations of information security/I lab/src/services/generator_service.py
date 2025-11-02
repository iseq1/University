from src.models.bent_function import BentFunction

class GeneratorService:
    """
    Генератор специальных булевых функций: bent, случайные, и т.п.
    """

    @staticmethod
    def generate_bent(n: int) -> BentFunction:
        """
        Генератор bent-функции по общему правилу:
        f = x1x2 ⊕ x3x4 ⊕ ... ⊕ x_{n-1}x_n
        Работает для любого чётного n.
        """
        if n % 2 != 0:
            raise ValueError("Bent-функции существуют только для чётного n")

        values = []
        for i in range(2**n):
            x = tuple(map(int, f"{i:0{n}b}"))
            val = 0
            for j in range(0, n, 2):
                val ^= (x[j] & x[j+1])
            values.append(val)

        # Формула (для наглядного вывода)
        formula = " ⊕ ".join([f"x{j+1}x{j+2}" for j in range(0, n, 2)])

        return BentFunction(n, values, description=formula)