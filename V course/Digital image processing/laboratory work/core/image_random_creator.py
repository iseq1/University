"""
Класс-обработчик построения изображения с взаимно независимыми амплитудами
"""
from abc import ABC, abstractmethod
import numpy as np
from scipy.ndimage import convolve


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

            if arr.ndim == 2:
                arr = np.stack([arr] * 3, axis=-1)

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


class ImageSmoothingHandler(ImageRandomHandler):
    """Генерация изображения методом скользящего суммирования"""

    @staticmethod
    def apply(h: int, w: int, dist_type: str, params: dict) -> dict:
        """
        Формирует изображение с применением скользящего суммирования
        :param h: число строк
        :param w: число столбцов
        :param dist_type: 'uniform' или 'normal'
        :param params:" параметры распределения и радиус окрестности
        :return: dict с изображением и параметрами
        """
        try:
            # Параметры для исходной сцены
            base = params.get('base', {'m': 127, 'sigma': 20})
            radius = int(params.get('radius', 1))

            # 1. Формируем исходную сцену
            base_result = ImageRandomHandler.apply(h, w, dist_type, base)
            if base_result['data'] is None:
                return base_result

            image = base_result['data']

            # 2. Скользящее суммирование по квадратной окрестности
            kernel = np.ones((2 * radius + 1, 2 * radius + 1), dtype=np.float32)
            kernel /= kernel.sum()  # теперь ядро усредняющее

            img_f = image.astype(np.float32)

            if img_f.ndim == 2:
                smoothed = convolve(img_f, kernel, mode='nearest')
            elif image.ndim == 3:
                smoothed = np.zeros_like(img_f, dtype=np.float32)
                for c in range(img_f.shape[2]):
                    smoothed[..., c] = convolve(img_f[..., c], kernel, mode='nearest')
            else:
                raise ValueError(f"Неподдерживаемая размерность изображения: {image.ndim}")

            smoothed_image = np.clip(smoothed, 0, 255).astype(np.uint8)

            # 3. Оценка среднего и дисперсии
            m_est = np.mean(smoothed_image)
            sigma_est = np.std(smoothed_image)

            return {
                'code': 'smooth_random_scene',
                'data': np.clip(smoothed_image, 0, 255).astype(np.uint8),
                'params': {'type': dist_type, 'radius': radius, 'base': base},
                'stats': {'m_est': float(m_est), 'sigma_est': float(sigma_est)},
                'msg': f'Сглаженная сцена {h}x{w} с радиусом {radius} успешно создана '
                       f'(m={m_est:.2f}, σ={sigma_est:.2f})'
            }

        except Exception as e:
            return {
                'code': 'smooth_random_scene',
                'data': None,
                'msg': f'Ошибка при построении сглаженной сцены: {e}'
            }
