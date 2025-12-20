"""
Реализация теста простоты Ферма
"""
from src.service.math_base import MathBase
import random

class FermatTest(MathBase):
    """Класс-обработчик реализующий тест простоты Ферма"""

    random.seed()

    def apply(self, x: int, steps: int = 5):
        """Применяет тест простоты Ферма к числу x на steps шагах"""
        if x in (2, 3):
            return True
        if x <= 1 or x % 2 == 0:
            return False

        for i in range(steps):
            a = random.randint(2, x - 2)
            if self.gcd(a, x) != 1:
                return False
            if self.pows(a, x - 1, x) != 1:
                return False
        return True
