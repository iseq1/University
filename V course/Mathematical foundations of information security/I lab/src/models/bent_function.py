# src/models/bent_function.py
from src.models.boolean_function import BooleanFunction

class BentFunction(BooleanFunction):
    """
    Представление bent-функции (частный случай BooleanFunction).
    По дизайну предполагаем, что переданный вектор действительно bent.
    Можно проверить вне при помощи NonlinearityService.
    """
    def __init__(self, n: int, values, description: str = ""):
        super().__init__(n, values)
        self.description = description

    def __repr__(self):
        desc = f", desc='{self.description}'" if self.description else ""
        return f"BentFunction(n={self.n}{desc})"
