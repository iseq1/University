"""
Представление линейной/аффинной булевой функции вида:
L(x) = a0 ⊕ a1*x1 ⊕ a2*x2 ⊕ ... ⊕ an*xn
"""

from src.models.boolean_function import BooleanFunction
from src.utils.vector_utils import get_all_inputs


class LinearFunction(BooleanFunction):

    def __init__(self, n: int, coeffs):
        """
        Создаёт аффинную функцию L(x) по набору её коэффициентов.

        :param n: число переменных
        :param coeffs: последовательность длины n+1
        :raises ValueError: если передано не n+1 коэффициентов
        """
        if len(coeffs) != n + 1:
            raise ValueError("Ожидается n+1 коэффициент (a0...an)")

        # Приводим коэффициенты к 0/1
        self.coeffs = [int(c) & 1 for c in coeffs]

        # Формируем вектор значений L(x)
        values = []
        inputs = get_all_inputs(n)  # все x ∈ F2^n MSB→LSB

        for x in inputs:
            # стартуем со свободного члена a0
            val = self.coeffs[0]

            # добавляем ai*xi (умножение AND, сумма XOR)
            for i in range(n):
                val ^= (self.coeffs[i + 1] & x[i])

            values.append(val)

        # создаём линейную ф-цию как обычную BooleanFunction
        super().__init__(n, values)


    def __repr__(self):
        return f"LinearFunction(coeffs={self.coeffs})"
