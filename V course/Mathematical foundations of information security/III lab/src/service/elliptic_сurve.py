"""
Реализация упрощенного теста простоты эллиптических кривых
"""
from src.service.math_base import MathBase
import random

class EllipticCurveTest(MathBase):
    """Класс-обработчик реализующий тест простоты посредством эллиптических кривых"""
    random.seed()

    def apply(self, n: int, k: int = 5):
        """Применяет тест эллиптических кривых к числу n."""
        if n <= 1:
            return False
        if n <= 3:
            return True

        # Выбираем случайное уравнение эллиптической кривой
        a = random.randint(1, n - 1)
        b = random.randint(1, n - 1)

        # Проверяем, что дискриминант не делится на n
        discriminant = (4 * a**3 + 27 * b**2) % n
        if discriminant == 0:
            return False

        # Выбираем случайную точку на кривой
        x = random.randint(1, n - 1)
        y = (x**3 + a * x + b) % n

        # Проверяем, что порядок точки делится на n
        # (Это упрощенная проверка, которая не всегда работает)
        for _ in range(k):
            point = (x, y)
            for _ in range(n):
                x, y = self.point_addition(point, (a, b), n)
                if x == 0 and y == 0:
                    return False
        return True


    def point_addition(self, point1: tuple[int, int], point2: tuple[int, int], n: int) -> tuple[int, int]:
        """Сложение точек на эллиптической кривой."""
        if point1 == (0, 0):
            return point2
        if point2 == (0, 0):
            return point1

        x1, y1 = point1
        x2, y2 = point2

        if x1 == x2 and y1 == -y2 % n:
            return 0, 0

        slope = ((y2 - y1) * self.pows(x2 - x1, -1, n)) % n
        x3 = (slope**2 - x1 - x2) % n
        y3 = (slope * (x1 - x3) - y1) % n
        return x3, y3
