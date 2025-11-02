from src.models.boolean_function import BooleanFunction

class BentFunction(BooleanFunction):
    """
    Представляет bent-функцию.
    Это частный случай булевой функции с максимальной нелинейностью.
    """
    def __init__(self, n: int, values: list[int], description: str = ""):
        super().__init__(n, values)
        self.description = description

    def __repr__(self):
        return f"BentFunction(n={self.n}, desc='{self.description}')"
