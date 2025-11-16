"""
Реализация теста простоты эллиптических кривых
"""
from src.service.math_base import MathBase


class EllipticCurveTest(MathBase):
    """Тест простоты эллиптических кривых"""


    def apply(self, n: int) -> bool:
        """
        Тест эллиптических кривых
        Найти P на y^2 = x^3+1 mod n. Посчитать (n+1)P.
        Если (n+1)P = бесконечность → n вероятно простое.
        """

        if n < 2:
            return False

        # Условие метода: n ≡ 2 mod 3  (для n ≡ 5 mod 6 подходит всегда)
        if n % 3 != 2:
            return False

        # Ищем точку P(x,y) на кривой y^2 = x^3 + 1 (mod n)
        P = None
        # небольшой диапазон
        for x in range(1, 200):
            rhs = (x ** 3 + 1) % n

            # ищем y такое, что y^2 == rhs mod n
            for y in range(1, 200):
                if (y * y) % n == rhs:
                    P = (x, y)
                    break
            if P:
                break

        if not P:
            # Не нашли подходящей P — число точно составное
            return False

        # P2 = (n + 1) * P
        P2 = self.point_mul(n + 1, P, n)

        # Если получили бесконечно удалённую точку -> n "простое"
        return P2 is None
