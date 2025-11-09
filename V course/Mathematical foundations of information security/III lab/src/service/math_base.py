"""
Реализация базовых математических операций
"""

class MathBase:
    """Базовые математические реализации"""

    def mul(self, a: int, b: int, m: int) -> int:
        """Вычисляет (a * b) % m, избегая переполнения."""
        if b == 1:
            return a
        if b % 2 == 0:
            t = self.mul(a, b // 2, m)
            return (2 * t) % m
        return (self.mul(a, b - 1, m) + a) % m

    def pows(self, a, b, m):
        """Быстрое возведение в степень по модулю (итеративно)."""
        result = 1
        a = a % m
        while b > 0:
            if b % 2 == 1:
                result = (result * a) % m
            a = (a * a) % m
            b //= 2
        return result

    def gcd(self, a: int, b: int) -> int:
        """Вычисляет наибольший общий делитель (НОД) двух чисел."""
        if b == 0:
            return a
        return self.gcd(b, a % b)
