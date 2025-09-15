from abc import ABC, abstractmethod
import numpy as np


class IByteConverter(ABC):
    """
    Абстрактный класс для представления класса взаимодействия с медиа файлами
    """
    @abstractmethod
    def to_bytes(self, gray_image: np.ndarray) -> tuple[bytes, str] | tuple[None, str]:
        """Преобразование RGB-изображения в градациях серого (из объекта типа Bitmap) в массив из объектов типа byte """
        pass

    @abstractmethod
    def from_bytes(self, gray_bytes: bytes, height: int, width: int) -> np.ndarray:
        """Преобразование массива из объектов типа byte в RGB-изображение в градациях серого (объект типа Bitmap)"""
        pass

class ByteConverter(IByteConverter):
    """
    Преобразование RGB-изображения (grayscale) в массив байтов и обратно.
    """

    def to_bytes(self, gray_image: np.ndarray) -> tuple[bytes, str] | tuple[None, str]:
        """Преобразование RGB-изображения в градациях серого (из объекта типа Bitmap) в массив из объектов типа byte """
        if np.all(gray_image[..., 0] == gray_image[..., 1]) and np.all(gray_image[..., 0] == gray_image[..., 2]):
            return gray_image[...,0].tobytes(), f'Сохранили {len(gray_image.tobytes())} байт'
        else:
            return None, f'Изображение не в оттенках серого!'


    def from_bytes(self, gray_bytes: bytes, height: int, width: int) -> tuple[None, str] | tuple[np.ndarray, str]:
        """Преобразование массива байтов в RGB NumPy-массив в градациях серого"""
        if not isinstance(gray_bytes, (bytes, bytearray)):
            return None, 'Нет массива байтов'

        arr = np.frombuffer(gray_bytes, dtype=np.uint8).reshape((height, width))
        rgb_array = np.stack([arr] * 3, axis=-1)
        return rgb_array, 'Восстановили изображение из массива байтов'