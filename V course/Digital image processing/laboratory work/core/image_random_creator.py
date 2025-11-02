"""
Класс-обработчик построения изображения с взаимно независимыми амплитудами
"""
from abc import ABC, abstractmethod
import numpy as np

class IImageRandomHandler(ABC):
    """Интерфейс обработчика"""

    @staticmethod
    @abstractmethod
    def apply(h: int, w: int, dist_type: str, params: dict) -> dict:
        pass

class ImageRandomHandler(IImageRandomHandler):
    """Генерация случайного изображения с заданным распределением амплитуд"""

    @staticmethod
    def apply(h: int, w: int, dist_type: str, params: dict) -> dict:
        """
        Формирует случайное изображение
        :param h: число строк
        :param w: число столбцов
        :param dist_type: 'uniform' или 'normal'
        :param params: параметры распределения
        :return: dict с изображением и параметрами
        """
        try:
            if dist_type == 'uniform':
                a, b = params.get('a', 0), params.get('b', 255)
                arr = np.random.uniform(a, b, (h, w))
            elif dist_type == 'normal':
                m, sigma = params.get('m', 127), params.get('sigma', 20)
                arr = np.random.normal(m, sigma, (h, w))
            else:
                raise ValueError("Неизвестный тип распределения")

            # Нормализация в диапазон [0,255]
            arr = np.clip(arr, 0, 255).astype(np.uint8)

            return {
                "code": "random_scene",
                "data": arr,
                "params": {"type": dist_type, **params},
                "msg": f"Сцена {h}x{w} с распределением {dist_type} успешно создана."
            }

        except Exception as e:
            return {
                "code": "random_scene",
                "data": None,
                "msg": f"Ошибка при построении сцены: {e}"
            }
