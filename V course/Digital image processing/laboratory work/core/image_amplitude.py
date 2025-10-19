"""
Класс-обработчик для взаимодействия с амплитудами определенных пикселей
"""
from abc import ABC, abstractmethod
import numpy as np

class IImageAmplitude(ABC):
    """Интерфейс обработчика амплитуды пикселя"""

    @staticmethod
    @abstractmethod
    def get_amplitude(array: np.ndarray, x: int, y: int) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def set_amplitude(array: np.ndarray, x: int, y: int, value) -> dict:
        pass


class ImageAmplitude(IImageAmplitude):
    """Обработчик измерения и изменения амплитуды пикселя"""

    @staticmethod
    def get_amplitude(array: np.ndarray, x: int, y: int) -> dict:
        """Получение амплитуды пикселя"""
        try:
            if array is None or not isinstance(array, np.ndarray):
                raise ValueError("Неверный тип входного массива")

            h, w = array.shape[:2]

            if not (0 <= x < w and 0 <= y < h):
                raise ValueError(f"Координаты ({x},{y}) вне изображения ({w}x{h})")

            if array.ndim == 2:
                amp = int(array[y, x])
            elif array.ndim == 3 and array.shape[2] >= 3:
                amp = tuple(int(v) for v in array[y, x][:3])
            else:
                raise ValueError("Неподдерживаемый формат изображения")

            return {
                "code": "amplitude_get",
                "data": amp,
                "msg": f"Амплитуда пикселя ({x},{y}) = {amp}"
            }

        except Exception as e:
            print(e)
            return {
                "code": "amplitude_get",
                "data": None,
                "msg": f"Ошибка при получении амплитуды: {e}"
            }

    @staticmethod
    def set_amplitude(array: np.ndarray, x: int, y: int, value) -> dict:
        """Изменение амплитуды пикселя"""
        try:
            if array is None or not isinstance(array, np.ndarray):
                raise ValueError("Неверный тип входного массива")

            h, w = array.shape[:2]

            if not (0 <= x < w and 0 <= y < h):
                raise ValueError(f"Координаты ({x},{y}) вне изображения ({w}x{h})")

            arr_copy = array.copy()

            if arr_copy.ndim == 2:  # grayscale
                val = np.clip(int(value), 0, 255)
                arr_copy[y, x] = val
            elif arr_copy.ndim == 3 and arr_copy.shape[2] >= 3:
                if isinstance(value, (tuple, list, np.ndarray)) and len(value) >= 3:
                    rgb = np.clip(np.array(value[:3], dtype=np.uint8), 0, 255)
                    arr_copy[y, x, :3] = rgb
                else:
                    raise ValueError("Для RGB изображения нужно передать 3 значения (R,G,B)")
            else:
                raise ValueError("Неподдерживаемый формат изображения")

            return {
                "code": "amplitude_set",
                "data": arr_copy,
                "msg": f"Амплитуда пикселя ({x},{y}) изменена на {value}"
            }

        except Exception as e:
            return {
                "code": "amplitude_set",
                "data": None,
                "msg": f"Ошибка при изменении амплитуды: {e}"
            }