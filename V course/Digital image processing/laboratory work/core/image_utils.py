import numpy as np
from PyQt6.QtGui import QImage, QPixmap

def pixmap_to_array(pixmap: QPixmap) -> np.ndarray:
    """Конвертирует QPixmap в NumPy-массив (H x W x 3, RGB)."""
    q_image = pixmap.toImage().convertToFormat(QImage.Format.Format_RGB888)
    width, height = q_image.width(), q_image.height()
    bytes_per_line = q_image.bytesPerLine()

    ptr = q_image.bits()
    ptr.setsize(q_image.sizeInBytes())

    arr = np.frombuffer(ptr, dtype=np.uint8).reshape((height, bytes_per_line // 3, 3))
    return arr[:, :width, :]  # обрезаем паддинг

# def array_to_pixmap(arr: np.ndarray) -> QPixmap:
#     """Конвертирует NumPy-массив (H x W x 3, RGB) в QPixmap."""
#     h, w, ch = arr.shape
#     assert ch == 3, "Ожидается RGB массив с 3 каналами"
#     bytes_per_line = ch * w
#     q_image = QImage(arr.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
#     return QPixmap.fromImage(q_image.copy())  # copy() чтобы избежать проблем с памятью


def array_to_pixmap(array: np.ndarray) -> QPixmap:
    h, w, ch = array.shape
    assert ch == 3, "Ожидается RGB массив с 3 каналами"
    bytes_per_line = ch * w
    # создаём QImage на основе сырых байтов
    q_image = QImage(
        array.tobytes(),  # именно байты, не memoryview
        w,
        h,
        bytes_per_line,
        QImage.Format.Format_RGB888
    )
    return QPixmap.fromImage(q_image.copy())
