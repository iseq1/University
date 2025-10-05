"""
Класс-обработчик для применения фильтра в градациях серого
"""
from abc import ABC, abstractmethod
import numpy as np

class IImageFilter(ABC):
    @abstractmethod
    def apply(self, array: np.ndarray) -> np.ndarray | None:
        pass

class Grayscale24Filter(IImageFilter):
    def __init__(self, mode: str = "bt601"):
        self.mode = mode  # "bt601", "average", "bt709"

    def apply(self, array: np.ndarray) -> np.ndarray | None:
        """Конвертирует RGB в 24-битные градации серого."""
        if array.size == 0:
            return None

        r, g, b = array[:, :, 0], array[:, :, 1], array[:, :, 2]

        if self.mode == "average":
            gray = (r + g + b) // 3
        elif self.mode == "bt709":
            gray = (0.2126 * r + 0.7152 * g + 0.0722 * b).astype(np.uint8)
        else:  # bt601
            gray = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)

        return np.stack([gray, gray, gray], axis=2)  # HWC, [G,G,G]
