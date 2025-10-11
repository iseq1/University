"""
Класс-обработчик для сглаживания амплитуд пикселей
"""
import numpy as np
from abc import ABC, abstractmethod


class IImageSmoothing(ABC):
    @staticmethod
    @abstractmethod
    def apply(array: np.ndarray, radius: int) -> dict:
        pass


class ImageSmoothing(IImageSmoothing):
    """Реализация ручного сглаживания (усреднения по квадратной окрестности)."""

    @staticmethod
    def apply(array: np.ndarray, radius: int = 1) -> dict:
        try:
            if array is None or not isinstance(array, np.ndarray):
                raise ValueError("Неверный тип входного массива")

            if radius < 1:
                raise ValueError("Радиус должен быть >= 1")

            img = array.astype(np.float32)
            h, w = img.shape[:2]
            smoothed = np.zeros_like(img)

            # чтобы не вылетать за границы — паддинг
            if img.ndim == 3:
                padded = np.pad(img, ((radius, radius), (radius, radius), (0, 0)), mode='reflect')
            else:
                padded = np.pad(img, ((radius, radius), (radius, radius)), mode='reflect')

            for y in range(h):
                for x in range(w):
                    y1, y2 = y, y + 2 * radius + 1
                    x1, x2 = x, x + 2 * radius + 1

                    region = padded[y1:y2, x1:x2]
                    smoothed[y, x] = np.mean(region, axis=(0, 1))

            smoothed = np.clip(smoothed, 0, 255).astype(np.uint8)

            return {
                "code": "smooth",
                "data": smoothed,
                "params": {"radius": radius},
                "msg": f"Сглаживание по квадратной окрестности (r={radius}) выполнено."
            }

        except Exception as e:
            print(f"Ошибка при ручном сглаживании: {e}")
            return {
                "code": "smooth",
                "data": None,
                "params": {"radius": radius},
                "msg": "Ошибка при выполнении сглаживания."
            }


# TYPE 2:

# class ImageSmoothing(IImageSmoothing):
#     """Сглаживание по квадратной окрестности с ускорением через интегральное изображение."""
#
#     @staticmethod
#     def apply(array: np.ndarray, radius: int = 1) -> dict:
#         try:
#             if array is None or not isinstance(array, np.ndarray):
#                 raise ValueError("Неверный тип входного массива")
#
#             if radius < 1:
#                 raise ValueError("Радиус должен быть >= 1")
#
#             img = array.astype(np.float32)
#             h, w = img.shape[:2]
#
#             # Если RGB — считаем для каждого канала отдельно
#             if img.ndim == 3:
#                 smoothed = np.zeros_like(img)
#                 for c in range(3):
#                     smoothed[..., c] = ImageSmoothing._mean_filter(img[..., c], radius)
#             else:
#                 smoothed = ImageSmoothing._mean_filter(img, radius)
#
#             smoothed = np.clip(smoothed, 0, 255).astype(np.uint8)
#
#             return {
#                 "code": "smooth",
#                 "data": smoothed,
#                 "params": {"radius": radius},
#                 "msg": f"Сглаживание (r={radius}) выполнено успешно."
#             }
#
#         except Exception as e:
#             print(f"Ошибка при сглаживании: {e}")
#             return {
#                 "code": "smooth",
#                 "data": None,
#                 "params": {"radius": radius},
#                 "msg": "Ошибка при выполнении сглаживания."
#             }
#
#     @staticmethod
#     def _mean_filter(channel: np.ndarray, radius: int) -> np.ndarray:
#         """Сглаживание одного канала через интегральное изображение (по формуле суммы площадей)."""
#         h, w = channel.shape
#
#         # добавляем паддинг для корректной обработки краёв
#         padded = np.pad(channel, ((radius, radius), (radius, radius)), mode='reflect')
#
#         # вычисляем интегральное изображение (накопленные суммы)
#         integral = np.cumsum(np.cumsum(padded, axis=0), axis=1)
#
#         # создаем смещённые окна для быстрого получения сумм
#         y1 = np.arange(0, h)
#         x1 = np.arange(0, w)
#         y2 = y1 + 2 * radius + 1
#         x2 = x1 + 2 * radius + 1
#
#         # итоговое усреднение
#         out = np.zeros_like(channel, dtype=np.float32)
#         area = (2 * radius + 1) ** 2
#
#         for i in range(h):
#             for j in range(w):
#                 y_low, x_low = i, j
#                 y_high, x_high = i + 2 * radius + 1, j + 2 * radius + 1
#                 s = (
#                     integral[y_high, x_high]
#                     - integral[y_low, x_high]
#                     - integral[y_high, x_low]
#                     + integral[y_low, x_low]
#                 )
#                 out[i, j] = s / area
#
#         return out
