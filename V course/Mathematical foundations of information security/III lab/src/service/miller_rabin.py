"""
Реализация теста простоты Миллера-Рабина
"""
from src.service.math_base import MathBase
import random

class MillerRabinTest(MathBase):
    """Класс-обработчик реализующий тест простоты Миллера-Рабина"""
    random.seed()

    def apply(self, n: int, k: int = 1):
        """Применяет тест простоты Миллера-Рабина к числу n на k повторах"""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0:
            return False

        s, r = 0, n - 1

        while r % 2 == 0:
            s += 1
            r //= 2

        for _ in range(k):
            a = random.randint(2, n - 2)
            x = self.pows(a, r, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(s - 1):
                x = self.pows(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True
