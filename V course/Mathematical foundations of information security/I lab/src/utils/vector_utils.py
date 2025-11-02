"""
Вспомогательные функции для взаимодействия с векторами
"""
from itertools import product
import numpy as np


def get_all_inputs(n: int) -> list:
    """
    Генерирует все бинарные векторы длины n
    :param n: Длина вектора
    :return: Список бинарных векторов
    """
    return list(product([0, 1], repeat=n))


def xor(a: int, b: int) -> int:
    """
    Побитовое сложение по модулю 2
    :param a: Первое число
    :param b: Второе число
    :return: Результат побитового сложения по модулю два
    """
    return (a + b) % 2


def get_hamming_distance(vec1: list, vec2: list) -> int:
    """
    Вычисляет расстояние Хэмминга между двумя векторами (или np-массивами).
    :param vec1: Первый вектор
    :param vec2: Второй вектор
    :return: Расстояние Хэмминга двух векторов
    """
    return np.sum(np.array(vec1) != np.array(vec2))
