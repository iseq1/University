"""
Класс-обработчик для построения изображения с кусочно-постоянными амплитудами
"""
from abc import ABC, abstractmethod
import numpy as np

class IImagePiecewiseHandler(ABC):
    """Интерфейс обработчика"""

    @staticmethod
    @abstractmethod
    def apply(array: np.ndarray, block_size: int = 8) -> dict:
        pass



class ImagePiecewiseHandler(IImagePiecewiseHandler):
    """Обработчик построения изображения с кусочно-постоянными амплитудами"""

    @staticmethod
    def apply(array: np.ndarray, block_size: int = 8) -> dict:
        try:
            h, w = array.shape[:2]
            result = np.zeros_like(array)

            for i in range(0, h, block_size):
                for j in range(0, w, block_size):
                    block = array[i:i+block_size, j:j+block_size]
                    mean_val = block.mean(axis=(0, 1), dtype=float)
                    result[i:i+block_size, j:j+block_size] = mean_val

            return {
                "code": "piecewise",
                "data": result.astype(np.uint8),
                "params": {"block_size": block_size},
                "msg": f"Создана кусочно-постоянная карта (размер блока = {block_size})"
            }

        except Exception as e:
            return {
                "code": "piecewise",
                "data": None,
                "msg": f"Ошибка при создании карты: {e}"
            }