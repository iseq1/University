"""
Класс-обработчик для вычисления статистики изображения
"""
from abc import ABC, abstractmethod
import numpy as np

class IImageStats(ABC):
    @staticmethod
    @abstractmethod
    def compute(array: np.ndarray, border_only: bool = False) -> dict:
        pass

class ImageStats(IImageStats):

    @staticmethod
    def compute(array: np.ndarray, border_only: bool = False) -> dict:
        """
        Вычисляет min, max, mean и std амплитуд для массива пикселей.
        Амплитуда = среднее значение (R, G, B).
        Если border_only=True, берём только границу массива.

        :param array: Изображение
        :param border_only: Граница изображения
        :return: Словарь статистики
        """
        try:
            if array.ndim != 3 or array.shape[2] < 3:
                raise ValueError("Ожидался массив вида (h, w, 3)")

            h, w, _ = array.shape

            if border_only:
                # верх и низ
                top = array[0, :, :]
                bottom = array[-1, :, :]
                # левый и правый край (без углов, чтобы не дублировать)
                left = array[1:-1, 0, :]
                right = array[1:-1, -1, :]
                border_pixels = np.vstack([top, bottom, left, right])
                pixels = border_pixels
            else:
                pixels = array.reshape(-1, 3)

            # амплитуда = среднее по каналам
            amplitudes = pixels.mean(axis=1)

            stats = {
                "min": round(float(np.min(amplitudes)), 2),
                "max": round(float(np.max(amplitudes)), 2),
                "mean": round(float(np.mean(amplitudes)), 2),
                "std": round(float(np.std(amplitudes)), 2),
            }

            return {
                'data': stats,
                'code': 'stat',
                'msg': 'Статистика изображения рассчитана успешно!',
            }
        except Exception as e:
            print(f'Произошла ошибка при вычислении статистики: {e}')
            return {
                'data': None,
                'code': 'stat',
                'msg': 'Статистика изображения не получена!',
            }