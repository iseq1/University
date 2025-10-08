"""
Класс-обработчик для применения линейного контрастирования
"""
from abc import ABC, abstractmethod
import numpy as np


class IImageLinearContrast(ABC):
    """Абстрактный интерфейс для линейного контрастирования."""

    @staticmethod
    @abstractmethod
    def apply(array: np.ndarray) -> dict:
        pass


class ImageLinearContrast(IImageLinearContrast):
    """Обработчик для применения линейного контрастирования."""

    @staticmethod
    def apply(array: np.ndarray) -> dict:
        """
        Применяет линейное контрастирование.
        :param array: NumPy ndarray (H, W, 3) или (H, W)
        :return: dict {
            'code': 'contrast',
            'data': np.ndarray,  # контрастированное изображение
            'stats': {'min': m, 'max': M},  # диапазон до контрастирования
            'msg': str
        }
        """
        try:
            if array is None or not isinstance(array, np.ndarray):
                raise ValueError("Неверный тип входного массива")

            # приводим к float для безопасных вычислений
            img = array.astype(np.float32)

            # Определяем диапазон
            m, M = np.min(img), np.max(img)
            if M == m:
                return {
                    'code': 'contrast',
                    'data': array.copy(),
                    'stats': {'min': float(m), 'max': float(M)},
                    'msg': 'Контрастирование не выполнено (равномерная яркость).'
                }

            # Линейное растяжение по формуле
            contrasted = 255.0 * (img - m) / (M - m)
            contrasted = np.clip(contrasted, 0, 255).astype(np.uint8)

            return {
                'code': 'contrast',
                'data': contrasted,
                'stats': {'min': float(m), 'max': float(M)},
                'msg': 'Линейное контрастирование успешно выполнено.'
            }

        except Exception as e:
            print(f"Ошибка при вычислении линейного контрастирования: {e}")
            return {
                'code': 'contrast',
                'data': None,
                'stats': None,
                'msg': 'Ошибка при вычислении линейного контрастирования.'
            }