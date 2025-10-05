"""
Классы-обработчик для открытия и сохранения изображений
"""
from abc import ABC, abstractmethod
from PIL import Image
import numpy as np


class IImageTransfer(ABC):
    """
    Абстрактный класс для представления класса взаимодействия с медиа файлами
    """
    @abstractmethod
    def load_image(self, file_path: str) -> np.ndarray | None:
        """Загрузить обрабатываемое изображение"""
        pass

    @abstractmethod
    def save_image(self, array: np.ndarray, file_path: str) -> bool:
        """Сохранить обрабатываемое изображение"""
        pass


class LocalImageTransfer(IImageTransfer):
    """Класс для взаимодействия с медиа файлами"""

    def load_image(self, file_path: str) -> np.ndarray | None:
        """Загружает изображение в NumPy-массив (RGB)."""
        try:
            img = Image.open(file_path).convert("RGB")  # всегда 3 канала
            return np.array(img)
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return None

    def save_image(self, arr: np.ndarray, file_path: str) -> None:
        """Сохраняет NumPy-массив (RGB) как изображение."""
        try:
            img = Image.fromarray(arr.astype(np.uint8), mode="RGB")
            img.save(file_path)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")