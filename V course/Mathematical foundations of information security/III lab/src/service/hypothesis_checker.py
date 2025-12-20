


class HypothesisChecker:
    """Проверка: EC отбрасывает все псевдопростые MR"""
    def __init__(self, pm):
        self.PrimeChecker = pm


    def check(self, limit: int):
        mr = self.PrimeChecker.fermat_test
        ec = self.PrimeChecker.elliptic_curve_test

        mr_pseudoprimes = []
        survived_both = []

        for n in range(limit):
            # честно определяем составность
            if HypothesisChecker.is_prime_naive(n):
                continue  # пропускаем простые

            # составное число
            if mr(n):
                mr_pseudoprimes.append(n)

                if ec(n):
                    survived_both.append(n)

        return mr_pseudoprimes, survived_both

    @staticmethod
    def is_prime_naive(n: int) -> bool:
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        return True


