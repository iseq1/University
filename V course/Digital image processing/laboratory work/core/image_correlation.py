"""
Класс-обработчик для оценки корреляционной функции
"""
from abc import ABC, abstractmethod
import numpy as np


class IImageCorrelationHandler(ABC):
    """
    Абстрактный класс для оценки корреляционной функции по изображению
    """

    @staticmethod
    @abstractmethod
    def apply(image: np.ndarray) -> dict:
        """Оценка корреляционной функции"""
        pass


class ImageCorrelationHandler(IImageCorrelationHandler):
    """Оценка корреляционной функции по изображению"""

    @staticmethod
    def apply(image: np.ndarray) -> dict:
        """Рассчитывает оценку корреляционной функции"""
        try:
            if image.ndim == 3:
                image = np.mean(image, axis=2)

            image = image.astype(float)
            image -= np.mean(image)

            f = np.fft.fft2(image)
            ps = np.abs(f) ** 2
            corr = np.fft.ifft2(ps).real
            corr = np.fft.fftshift(corr)
            corr /= np.max(corr)

            return {
                "code": "correlation_random_scene",
                "data": corr,
                "msg": f"Корреляционная функция успешно вычислена"
            }

        except Exception as e:
            return {
                "code": "correlation_random_scene",
                "data": None,
                "msg": f"Ошибка при вычислении: {e}"
            }