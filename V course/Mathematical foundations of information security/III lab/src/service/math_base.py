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

    def inv_mod(self, a, n):
        """Обратный элемент по модулю n."""
        try:
            return pow(a, -1, n)
        except ValueError:
            return None

    def point_add(self, P, Q, n):
        """Сложение точек P и Q на кривой y^2 = x^3 + 1 (mod n)."""

        # Точка на бесконечности
        if P is None:
            return Q
        if Q is None:
            return P

        x1, y1 = P
        x2, y2 = Q

        # P + (-P) = O
        if (x1 == x2) and ((y1 + y2) % n == 0):
            return None

        if P != Q:
            # Формула сложения
            inv = self.inv_mod(x2 - x1, n)
            if inv is None:
                return None
            s = ((y2 - y1) * inv) % n
        else:
            # Формула удвоения
            inv = self.inv_mod(2 * y1, n)
            if inv is None:
                return None
            s = (3 * x1 * x1 * inv) % n

        x3 = (s * s - x1 - x2) % n
        y3 = (s * (x1 - x3) - y1) % n

        return x3, y3

    def point_mul(self, k, P, n):
        """Умножение точки P на число k."""
        R = None
        Q = P
        while k > 0:
            if k & 1:
                R = self.point_add(R, Q, n)
            Q = self.point_add(Q, Q, n)
            k >>= 1
        return R