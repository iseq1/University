import secrets
from math import gcd

from Miller_Rabin import miller_rabin_test


def generate_prime_candidate(length):
    """
    Генерирует случайное нечетное число длиной length бит, которое может быть кандидатом на простое число.

    Args:
        length (int): Длина в битах для генерируемого числа.

    Returns:
        int: Случайное число длиной length бит.
    """
    # Генерация случайного числа длиной length бит
    p = secrets.randbits(length)
    # Установка старшего бита для обеспечения нужной длины числа
    # Установка младшего бита для обеспечения нечетности числа
    # p = 5 = 0101
    # l = 4 -> length - 1 = 3
    # p = 0101 OR 1000 OR 0001 = 1110 -> 13
    p |= (1 << (length - 1)) | 1
    return p



def generate_prime(length):
    """
    Генерирует простое число длиной length бит, используя тест Миллера-Рабина.

    Args:
        length (int): Длина в битах для простого числа.

    Returns:
        int: Простое число длиной length бит.
    """
    p = 4  # не простое число
    # генерация простого числа до тех пор, пока не будет найдено подходящее
    while not miller_rabin_test(p, 40):
        p = generate_prime_candidate(length)
    return p


def mod_inverse(a, m):
    """
    Вычисляет мультипликативную обратную величину a по модулю m, используя расширенный алгоритм Евклида.

    Args:
        a (int): Число, для которого находится обратное значение.
        m (int): Модуль.

    Returns:
        int: Мультипликативная обратная величина a по модулю m.
    """
    # Сохраняем значение m для окончательной коррекции
    b, s, t = m, 0, 1
    if m == 1:
        return 0 # Обратного значения не существует

    # Расширенный алгоритм Евклида
    while a > 1:
        #  q - частное от деления a на m
        q = a // m
        # Обновление m и a по алгоритму Евклида
        m, a = a % m, m
        # Обновление коэффициентов s и t
        s, t = t - q * s, s
    # Если t отрицательно, корректируем его значение
    if t < 0:
        t += b
    return t


def generate_rsa_keys(bit_length):
    """
    Генерирует пару RSA ключей (публичный и приватный) заданной длины.

    Args:
        bit_length (int): Длина ключа в битах.

    Returns:
        tuple: Пара (публичный ключ, приватный ключ). Каждый ключ представлен как кортеж (экспонента, модуль).
    """
    # Генерация первого простого числа p
    p = generate_prime(bit_length)
    # Генерация второго простого числа q, не равного p
    q = generate_prime(bit_length)
    while q == p:
        q = generate_prime(bit_length)

    # вычисление модуля n
    n = p * q
    # вычисление функции Эйлера phi
    phi = (p - 1) * (q - 1)
    # выбор открытой экспоненты e
    e = 65537
    # проверяем, что e и phi взаимно просты
    while gcd(e, phi) != 1:
        e += 2

    # Вычисление приватной экспоненты d
    d = mod_inverse(e, phi)

    # Возвращение пары ключей (публичный и приватный)
    return (e, n), (d, n)


def rsa_encrypt_block(m, e, n):
    """
    Шифрует блок данных с использованием публичного ключа RSA.

    Args:
        m (int): Блок данных для шифрования.
        e (int): Публичная экспонента.
        n (int): Модуль.

    Returns:
        int: Зашифрованный блок данных.
    """
    # возведение блока данных m в степень e по модулю n для шифрования
    return pow(m, e, n)


def rsa_decrypt_block(c, d, n):
    """
    Дешифрует блок данных с использованием приватного ключа RSA.

    Args:
        c (int): Зашифрованный блок данных.
        d (int): Приватная экспонента.
        n (int): Модуль.

    Returns:
        int: Дешифрованный блок данных.
    """
    # возведение зашифрованного блока c в степень d по модулю n для дешифрования
    return pow(c, d, n)


def pad_block(block, block_size):
    """
    Дополняет блок данных до заданного размера нулями.

    Args:
        block (bytes): Блок данных.
        block_size (int): Желаемый размер блока.

    Returns:
        bytes: Дополненный блок данных.
    """
    # Вычисление длины дополнения (сколько байтов не хватает до block_size)
    pad_len = block_size - len(block)
    # Создание байтовой строки дополнения из нулевых байтов
    padding = bytes([0] * pad_len)
    # Возвращение дополненного блока данных, с добавлением нулевых байтов в начало
    return padding + block


def add_random_padding(block, block_size):
    """
    Добавляет случайный байт в конец блока данных.

    Args:
        block (bytes): Блок данных.
        block_size (int): Размер блока.

    Returns:
        bytes: Блок данных с добавленным случайным байтом.
    """
    # Генерация случайного байта для дополнения блока
    padding_byte = secrets.token_bytes(1)
    # Возвращение блока данных с добавлением случайного байта в конец
    return block + padding_byte


def rsa_encrypt(text, public_key, m):
    """
    Шифрует текст с использованием публичного ключа RSA и блочного шифрования.

    Args:
        text (str): Текст для шифрования.
        public_key (tuple): Публичный ключ (экспонента, модуль).
        block_size (int): Размер блока в битах.

    Returns:
        bytes: Зашифрованный текст.
    """
    e, n = public_key
    # Кодирование текста в байты
    byte_text = text.encode()
    # Вычисление длины блока данных в байтах
    block_length = (m // 8) - 1

    R = []

    for i in range(0, len(byte_text), block_length):
        # Выделение очередного блока данных
        # v_i блок
        block = byte_text[i:i + block_length]
        # Дополнение блока данных до нужной длины - добавляем ноль, чтобы было потом куда добавлять старший байт
        padded_block = pad_block(block, block_length + 1)
        # Добавление случайного дополнения - случайно добавляется в начало старший байт
        padded_block_with_random = add_random_padding(padded_block, m // 8)
        # Преобразование блока данных в целое число
        h = int.from_bytes(padded_block_with_random, byteorder='big')
        # Шифрование блока данных с использованием RSA
        r = rsa_encrypt_block(h, e, n)
        # Преобразование зашифрованного блока в последовательность байтов
        encrypted_block = r.to_bytes(m // 8, byteorder='big')
        # Добавление зашифрованного блока в список зашифрованных блоков
        R.append(encrypted_block)

    # Объединение всех зашифрованных блоков в один байтовый объект
    return b''.join(R)


def remove_random_padding(block):
    """
   Удаляет случайный байт из конца блока данных.

   Args:
       block (bytes): Блок данных.

   Returns:
       bytes: Блок данных без случайного байта.
   """
    return block[:-1]


def rsa_decrypt(encrypted_text, private_key, block_size):
    """
   Дешифрует зашифрованный текст с использованием приватного ключа RSA и блочного шифрования.

   Args:
       encrypted_text (bytes): Зашифрованный текст.
       private_key (tuple): Приватный ключ (экспонента, модуль).
       block_size (int): Размер блока в битах.

   Returns:
       str: Дешифрованный текст.
   """
    d, n = private_key
    # Определение размера блока данных в байтах
    block_size_bytes = block_size // 8
    decrypted_bytes = []

    for i in range(0, len(encrypted_text), block_size_bytes):
        # Выделение очередного зашифрованного блока
        block = encrypted_text[i:i + block_size_bytes]
        # Преобразование зашифрованного блока в целое число
        r = int.from_bytes(block, byteorder='big')
        # Дешифрование блока данных с использованием RSA
        h = rsa_decrypt_block(r, d, n)
        # Преобразование дешифрованного блока в последовательность байтов
        decrypted_block = h.to_bytes(block_size_bytes, byteorder='big')
        # Удаление случайного дополнения блока
        decrypted_block_without_padding = remove_random_padding(decrypted_block)
        # Добавление дешифрованного блока в список дешифрованных блоков
        decrypted_bytes.append(decrypted_block_without_padding)

    # Объединение всех дешифрованных блоков в один байтовый объект
    t = b''.join(decrypted_bytes)

    # Удаление ведущего нулевого дополнения, добавленного во время шифрования
    first_non_zero = next((i for i, b in enumerate(t) if b != 0), len(t))
    t = t[first_non_zero:]

    # Декодирование дешифрованного текста в строку
    return t.decode()
