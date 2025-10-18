"""
Класс-обработчик масштабирования изображения
"""
import numpy as np
from abc import ABC, abstractmethod


class IImageScale(ABC):
    """Интерфейс для изменения масштаба изображения"""

    @staticmethod
    @abstractmethod
    def apply(array: np.ndarray, scale_x: float, scale_y: float, method: str = 'nearest') -> dict:
        pass


class ImageScale(IImageScale):
    """Реализация масштабирования двумя методами"""

    @staticmethod
    def apply(array: np.ndarray, scale_x: float, scale_y: float, method: str = 'nearest') -> dict:
        """
        Масштабирует изображение методом ближайшего соседа или билинейной интерполяции.
        :param array: NumPy ndarray (H, W[, 3])
        :param scale_x: масштаб по ширине
        :param scale_y: масштаб по высоте
        :param method: 'nearest' или 'bilinear'
        :return: dict с результатом
        """
        try:
            if array is None or not isinstance(array, np.ndarray):
                raise ValueError("Неверный тип входного массива")

            if scale_x <= 0 or scale_y <= 0:
                raise ValueError("Масштаб должен быть положительным")

            h, w = array.shape[:2]
            new_h, new_w = int(h * scale_y), int(w * scale_x)

            if method == 'nearest':
                scaled = ImageScale._nearest(array, new_h, new_w)
            elif method == 'bilinear':
                scaled = ImageScale._bilinear(array, new_h, new_w)
            else:
                raise ValueError(f"Неизвестный метод масштабирования: {method}")

            return {
                'code': 'scale',
                'data': scaled,
                'params': {'scale_x': scale_x, 'scale_y': scale_y, 'method': method},
                'msg': f'Масштабирование ({method}) выполнено: ({w},{h}) → ({new_w},{new_h})'
            }

        except Exception as e:
            print(f"Ошибка при масштабировании: {e}")
            return {'code': 'scale', 'data': None, 'msg': str(e)}


    @staticmethod
    def _nearest(array: np.ndarray, new_h: int, new_w: int) -> np.ndarray:
        """Масштабирование методом ближайшего соседа (выборки)"""
        h, w = array.shape[:2]
        y_idx = (np.arange(new_h) * (h / new_h)).astype(int)
        x_idx = (np.arange(new_w) * (w / new_w)).astype(int)
        y_idx = np.clip(y_idx, 0, h - 1)
        x_idx = np.clip(x_idx, 0, w - 1)

        if array.ndim == 3:
            return array[y_idx[:, None], x_idx[None, :], :]
        else:
            return array[y_idx[:, None], x_idx[None, :]]

    @staticmethod
    def _bilinear(array: np.ndarray, new_h: int, new_w: int) -> np.ndarray:
        """Масштабирование методом билинейной интерполяции"""
        h, w = array.shape[:2]
        y = np.linspace(0, h - 1, new_h)
        x = np.linspace(0, w - 1, new_w)
        x_grid, y_grid = np.meshgrid(x, y)

        x1 = np.floor(x_grid).astype(int)
        y1 = np.floor(y_grid).astype(int)
        x2 = np.clip(x1 + 1, 0, w - 1)
        y2 = np.clip(y1 + 1, 0, h - 1)

        a = x_grid - x1
        b = y_grid - y1

        if array.ndim == 3:
            result = np.zeros((new_h, new_w, 3), dtype=np.float32)
            for c in range(3):
                I11 = array[y1, x1, c]
                I21 = array[y1, x2, c]
                I12 = array[y2, x1, c]
                I22 = array[y2, x2, c]
                result[..., c] = (
                        (1 - a) * (1 - b) * I11 +
                        a * (1 - b) * I21 +
                        (1 - a) * b * I12 +
                        a * b * I22
                )
        else:
            I11 = array[y1, x1]
            I21 = array[y1, x2]
            I12 = array[y2, x1]
            I22 = array[y2, x2]
            result = (
                    (1 - a) * (1 - b) * I11 +
                    a * (1 - b) * I21 +
                    (1 - a) * b * I12 +
                    a * b * I22
            )

        return np.clip(result, 0, 255).astype(np.uint8)

    @staticmethod
    def scale_roi_rect(roi_rect, scale_x, scale_y):
        """Масштабирует ROI (x, y, w, h)"""
        if roi_rect is None:
            return None
        x, y, w, h = roi_rect
        return int(x * scale_x), int(y * scale_y), int(w * scale_x), int(h * scale_y)
