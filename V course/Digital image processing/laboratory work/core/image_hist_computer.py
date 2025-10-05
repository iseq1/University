"""
Класс-обработчик для вычисления гистограммы
"""
import numpy as np
from abc import ABC, abstractmethod
from collections import Counter

class IImageHistogram(ABC):
    @staticmethod
    @abstractmethod
    def compute(array: np.ndarray, border_only: bool = False) -> dict:
        pass


class ImageHistogram(IImageHistogram):
    """Обработчик для вычисления и построения гистограммы пикселей."""

    @staticmethod
    def compute(array: np.ndarray, border_only: bool = False) -> dict:
        """
        Строим гистограмму амплитуд пикселей.
        :param array: NumPy-массив изображения
        :param border_only: только по границе ROI
        :return: Словарь с нормализованными значениями
        """
        try:
            if array.ndim == 3 and array.shape[2] == 3:
                # амплитуда = среднее R,G,B
                gray = array.mean(axis=2).astype(np.uint8)
            else:
                gray = array.astype(np.uint8)

            if border_only:
                # берём только границу
                mask = np.zeros_like(gray, dtype=bool)
                print(mask.shape)
                mask[0, :] = mask[-1, :] = mask[:, 0] = mask[:, -1] = True
                print(mask.shape)
                pixels = gray[mask]
            else:
                pixels = gray.flatten()

            total = len(pixels)
            counter = Counter(pixels)
            hist = {y: count / total for y, count in counter.items()}

            return {
                "code": "hist",
                "data": hist,
                "pixels": pixels,
                'msg': 'Гистограмма изображения рассчитана успешно!',
            }

        except Exception as e:
            print(f"Ошибка при вычислении гистограммы: {e}")
            return {
                "code": "hist",
                "data": None,
                "pixels": None,
                'msg': 'Гистограмма изображения не получена!',
            }