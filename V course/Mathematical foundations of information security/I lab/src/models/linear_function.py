# src/models/linear_function.py
from src.models.boolean_function import BooleanFunction
from src.utils.vector_utils import get_all_inputs

class LinearFunction(BooleanFunction):
    """
    Линейная/аффинная функция f(x) = a0 + a1*x1 + ... + an*xn (mod 2)
    coeffs: список длины n+1: [a0, a1, ..., an]
    """
    def __init__(self, n: int, coeffs):
        if len(coeffs) != n + 1:
            raise ValueError("Ожидается n+1 коэффициент (a0...an)")
        self.coeffs = [int(c) & 1 for c in coeffs]
        # создаём вектор значений в том же порядке, что и BooleanFunction
        values = []
        inputs = get_all_inputs(n)  # кортежи MSB..LSB
        for x in inputs:
            val = self.coeffs[0]
            # ai * xi суммируем по модулю 2
            for i in range(n):
                val ^= (self.coeffs[i + 1] & x[i])
            values.append(val)
        super().__init__(n, values)

    def __repr__(self):
        return f"LinearFunction(coeffs={self.coeffs})"
