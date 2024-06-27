import random
import math

# Кастомная функция для быстрого
# возведения в степень длинных чисел по модулю.
def power_mod(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result


# Алгоритм Миллера-Робина
def miller_rabin_test(n, rounds):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    def check(a, s, d, n):
        x = power_mod(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                return True
        return False

    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(rounds):
        a = random.randint(2, n - 2)
        if not check(a, s, d, n):
            return False
    return True

# функцию, которая генерирует (возможно) простое
# число определенной битности.
def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        p |= (1 << bits - 1) | 1
        if miller_rabin_test(p, 10):
            return p

def is_prime(p, n=None):
    if n is None:
        n = math.ceil(math.log2(p))
    return miller_rabin_test(p, n)


def fi(n):
    if is_prime(n):
        f = n;
        if n%2 == 0:
            while n%2 == 0:
                n = n // 2;
            f = f // 2;
        i = 3
        while i*i <= n:
            if n%i == 0:
                while n%i == 0:
                    n = n // i;
                f = f // i;
                f = f * (i-1);
            i = i + 2;
        if n > 1:
            f = f // n;
            f = f * (n-1);
        return f;
    return


for i in range(2,1001):
    if fi(i):
        print(f'Number {i} - {fi(i)}')




