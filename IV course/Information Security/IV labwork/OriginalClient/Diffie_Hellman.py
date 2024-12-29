import random


class DiffieHellman():
    def __init__(self, a=None, b=None, g=None, p=None):
        self.a = self.generate_odd_64bit() if a is None else a
        self.b = self.generate_odd_64bit() if b is None else b
        self.g = self.generate_generator() if g is None else g
        self.p = self.generate_prime_512bit() if p is None else p



    def make_A(self):
        """ A = g^a mod p """
        return self.mod_exp(base=self.g, exp=self.a, mod=self.p)

    def make_B(self):
        """ B = g^b mod p """
        return self.mod_exp(base=self.g, exp=self.b, mod=self.p)

    def make_K(self, base, exp, mod):
        return self.mod_exp(base=base, exp=exp, mod=mod)

    def generate_prime_512bit(self) -> int:
        """
        Генерация 512-битного простого числа методом Соловея-Штрассена.

        Алгоритм:
        1. Генерируем случайное 512-битное нечетное число
        2. Проверяем его на простоту тестом Соловея-Штрассена
        3. Повторяем пока не найдем простое число
        """
        while True:
            # Генерируем случайное 512-битное число
            # getrandbits(512) дает случайное число указанной длины
            # | 1 гарантирует, что число будет нечетным (последний бит = 1)
            num = random.getrandbits(512) | 1

            # Проверяем, что число действительно 512-битное
            # Если получилось меньше, устанавливаем старший бит
            if num < 2 ** 511:
                # (1 << 511) создает число с 1 в 512-й позиции
                # | устанавливает этот бит в num
                num |= (1 << 511)

            # Проверяем число на простоту тестом Соловея-Штрассена
            if self.solovay_strassen_test(num):
                return num

    def mod_exp(self, base: int, exp: int, mod: int) -> int:
        """
        Быстрое возведение в степень по модулю.
        base - основание
        exp - показатель степени
        mod - модуль
        """
        # Особый случай - при модуле 1 всегда получаем 0
        # Любое число по модулю 1 всегда дает 0
        if mod == 1:
            return 0

        # Начальное значение результата
        result = 1
        # Приводим базу по модулю для оптимизации
        base = base % mod

        # Пока показатель степени не станет равным 0
        while exp > 0:
            # Если текущий бит показателя равен 1
            # (проверяем с помощью побитового И)
            if exp & 1:
                # Умножаем результат на текущую базу
                result = (result * base) % mod

            # Возводим базу в квадрат для следующей итерации
            base = (base * base) % mod
            # Сдвигаем показатель вправо (делим на 2)
            exp >>= 1

        return result

    def jacobi_symbol(self, a: int, n: int) -> int:
        """
        Вычисление символа Якоби (a/n).
        Символ Якоби равен:
         0 если a и n имеют общий делитель
        +1 если a является квадратичным вычетом по модулю n
        -1 если a является квадратичным невычетом по модулю n

        Пусть p - простое нечетное число. Тогда число a, такое, что НОД(a, p) = 1,
        называется вычетом степени n, если:

            x^n = a (mod p)

        В обратном случае число a называется невычетом степени n. При n = 2 вычет a наз-ся квадратичным.

        Args:
            a (int): Верхнее число
            n (int): Нижнее число (должно быть нечетным положительным)

        Returns:
            int: Значение символа Якоби (-1, 0 или 1)
        """
        # Базовые случаи
        if a == 0:  # Если a = 0, символ Якоби = 0
            return 0
        if a == 1:  # Если a = 1, символ Якоби = 1
            return 1

        # Свойство 1: Если a отрицательное
        # (a/n) = (-1)^((n-1)/2) * (-a/n)
        if a < 0:
            return (-1) ** ((n - 1) // 2) * self.jacobi_symbol(-a, n)

        # Свойство 2: Если a четное
        # (2/n) = (-1)^((n^2-1)/8)
        if a % 2 == 0:
            return (-1) ** ((n * n - 1) // 8) * self.jacobi_symbol(a // 2, n)

        # Свойство 3: Если a >= n, можно взять остаток
        if a >= n:
            return self.jacobi_symbol(a % n, n)

        # Свойство 4: Квадратичный закон взаимности
        # Для двух различных нечетных простых чисел a и n символы Якоби связаны формулой:
        # (a/n) = (-1)^((a-1)(n-1)/4) * (n/a)
        return (-1) ** ((a - 1) * (n - 1) // 4) * self.jacobi_symbol(n % a, a)

    def solovay_strassen_test(self, n: int, k: int = 10) -> bool:
        """
        Вероятностный тест на простоту числа методом Соловея-Штрассена.

        Принцип работы:
        Для простого числа n и любого числа a, взаимно простого с n:
        a^((n-1)/2) ≡ (a/n) (mod n), где (a/n) - символ Якоби

        Args:
            n (int): Тестируемое число
            k (int): Количество раундов тестирования (больше k = выше точность)

        Returns:
            bool: True если число вероятно простое, False если составное
        """
        # Проверка базовых случаев
        if n == 2:
            return True
        if n < 2 or n % 2 == 0:  # Четные числа кроме 2 не простые
            return False

        # Проводим k раундов тестирования
        for _ in range(k):
            # Выбираем случайное число a из интервала [2, n-1]
            a = random.randrange(2, n)

            # Вычисляем символ Якоби (a/n)
            x = self.jacobi_symbol(a, n)

            # Если x = 0, значит a и n имеют общий делитель => n составное
            # Если a^((n-1)/2) mod n ≠ символу Якоби mod n, то n составное
            if x == 0 or self.mod_exp(a, (n - 1) // 2, n) != (x % n):
                return False

        # Если все тесты пройдены, число вероятно простое
        # Вероятность ошибки не более 1/2^k
        return True

    def is_sophie_germain_prime(self, p: int) -> bool:
        """
        Проверка является ли число простым числом Софи Жермен.
        Число p является числом Софи Жермен, если:
        1. p - простое число
        2. 2p + 1 - тоже простое число

        Args:
            p (int): Проверяемое число

        Returns:
            bool: True если число является числом Софи Жермен, False иначе
        """
        # Сначала проверяем, является ли p простым
        if not self.solovay_strassen_test(p):
            return False
        # Затем проверяем, является ли 2p + 1 простым
        return self.solovay_strassen_test(2 * p + 1)

    def generate_sophie_germain_primes(self, count: int) -> list:
        """
        Генерация заданного количества чисел Софи Жермен.

        Args:
            count (int): Требуемое количество чисел

        Returns:
            list: Список чисел Софи Жермен
        """
        primes = []
        # Начинаем с 3, так как 2 не подходит
        candidate = 3
        while len(primes) < count:
            # Проверяем каждое число на соответствие условиям
            if self.is_sophie_germain_prime(candidate):
                primes.append(candidate)
            # Увеличиваем на 2, так как четные числа (кроме 2)
            # не могут быть простыми
            candidate += 2
        return primes

    def generate_generator(self) -> int:
        """
        Генерация генератора группы (числа Софи Жермен).
        Число p является числом Софи Жермен, если:
        1. p - простое число
        2. 2p + 1 - тоже простое число

        """
        primes = self.generate_sophie_germain_primes(10)  # Генерируем 10 чисел Софи Жермен
        return random.choice(primes)

    def generate_odd_64bit(self) -> int:
        """Генерация 64-битного нечетного числа."""
        num = random.getrandbits(64)
        if num % 2 == 0:
            num += 1
        return num