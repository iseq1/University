"""
Класс-обработчик для поворота изображения
"""
import numpy as np
from abc import ABC, abstractmethod


class IImageRotate(ABC):
    @staticmethod
    @abstractmethod
    def apply(array: np.ndarray, angle_deg: float) -> dict:
        pass


class ImageRotate(IImageRotate):
    """Реализация поворота изображения"""

    @staticmethod
    def apply(array: np.ndarray, angle_deg: float) -> dict:
        """
        Поворот изображения на угол angle_deg вручную.
        :param array: Исходное изображение (H, W) или (H, W, 3)
        :param angle_deg: угол в градусах
        :return: повернутое изображение (np.uint8)
        """
        try:
            if array is None or not isinstance(array, np.ndarray):
                raise ValueError("Неверный тип входного массива")

            h, w = array.shape[:2]
            angle = np.deg2rad(angle_deg)

            cos_a, sin_a = np.cos(angle), np.sin(angle)

            # --- вычисляем новые размеры
            new_w = int(abs(w * cos_a) + abs(h * sin_a))
            new_h = int(abs(w * sin_a) + abs(h * cos_a))

            # --- создаём пустое изображение
            if array.ndim == 3:
                rotated = np.zeros((new_h, new_w, 3), dtype=np.uint8)
            else:
                rotated = np.zeros((new_h, new_w), dtype=np.uint8)

            # --- центры старого и нового изображений
            cx_old, cy_old = w / 2, h / 2
            cx_new, cy_new = new_w / 2, new_h / 2

            for y in range(new_h):
                for x in range(new_w):
                    # обратная трансформация
                    x_rel = x - cx_new
                    y_rel = y - cy_new

                    x_src = cos_a * x_rel + sin_a * y_rel + cx_old
                    y_src = -sin_a * x_rel + cos_a * y_rel + cy_old

                    if 0 <= x_src < w and 0 <= y_src < h:
                        rotated[y, x] = array[int(y_src), int(x_src)]

            return {
                "code": "rotate",
                "data": rotated,
                'stats': {'angle': angle_deg, 'new_size': (new_w, new_h)},
                "msg": f"Поворот изображения на {angle_deg} градусов выполнен."
            }

        except Exception as e:
            print(f"Ошибка при повороте: {e}")
            return {
                "code": "smooth",
                "data": None,
                "params": {"angle": angle_deg},
                "msg": "Ошибка при выполнении поворота."
            }

    @staticmethod
    def rotate_roi_rect(roi_rect, old_shape, angle_deg):
        """Поворачивает ROI (x, y, w, h) вместе с изображением без смещения"""
        if roi_rect is None:
            return None

        x, y, w, h = roi_rect
        h_old, w_old = old_shape[:2]

        angle = np.deg2rad(angle_deg)
        cos_a, sin_a = np.cos(angle), np.sin(angle)

        # новые размеры (такие же как при повороте изображения)
        new_w = int(abs(w_old * cos_a) + abs(h_old * sin_a))
        new_h = int(abs(w_old * sin_a) + abs(h_old * cos_a))

        # центры
        cx_old, cy_old = w_old / 2, h_old / 2
        cx_new, cy_new = new_w / 2, new_h / 2

        # матрица поворота
        rot = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])

        # углы ROI
        corners = np.array([
            [x, y],
            [x + w, y],
            [x + w, y + h],
            [x, y + h]
        ])

        # сдвигаем относительно старого центра → поворачиваем → добавляем сдвиг из-за новой системы
        centered = corners - np.array([cx_old, cy_old])
        rotated = centered @ rot.T + np.array([cx_new, cy_new])

        # новый bounding box
        x_min, y_min = rotated[:, 0].min(), rotated[:, 1].min()
        x_max, y_max = rotated[:, 0].max(), rotated[:, 1].max()

        return int(x_min), int(y_min), int(x_max - x_min), int(y_max - y_min)
