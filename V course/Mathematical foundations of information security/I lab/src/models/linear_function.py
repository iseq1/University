"""
Класс представление линейной функции
"""
from src.models.boolean_function import BooleanFunction
from src.utils.vector_utils import xor

class LinearFunction(BooleanFunction):
    """
    Класс для линейных (аффинных) функций:
    f(x) = a0 + a1*x1 + a2*x2 + ... + an*xn (mod 2)
    """

    def __init__(self, n: int, coeffs: list[int]):
        if len(coeffs) != n + 1:
            raise ValueError("Ожидается n+1 коэффициент (a0...an)")
        self.coeffs = coeffs
        self.n = n

        values = []
        for i in range(2 ** n):
            x = tuple(map(int, f"{i:0{n}b}"))
            res = coeffs[0]
            for j in range(n):
                res = xor(res, coeffs[j + 1] * x[j])
            values.append(res)

        super().__init__(n, values)

    def __repr__(self):
        return f"LinearFunction(coeffs={self.coeffs})"
