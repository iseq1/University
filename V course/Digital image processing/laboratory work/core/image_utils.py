"""
Вспомогательные функции для взаимодействия с изображением
"""
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PyQt6.QtGui import QImage, QPixmap

def pixmap_to_array(pixmap: QPixmap) -> np.ndarray:
    """
    Конвертирует QPixmap в NumPy-массив (H x W x 3, RGB).

    :param pixmap: Изображение формата QPixmap
    :return: Изображение в формате numpy-массива
    """
    q_image = pixmap.toImage().convertToFormat(QImage.Format.Format_RGB888)
    width, height = q_image.width(), q_image.height()
    bytes_per_line = q_image.bytesPerLine()

    ptr = q_image.bits()
    ptr.setsize(q_image.sizeInBytes())

    arr = np.frombuffer(ptr, dtype=np.uint8).reshape((height, bytes_per_line // 3, 3))
    return arr[:, :width, :]  # обрезаем паддинг


def array_to_pixmap(array: np.ndarray) -> QPixmap:
    """
    Конвертирует Numpy-массив (H x W x 3, RGB) в QPixmap

    :param array: Изображение в формате numpy-массива
    :return: Изображение формата QPixmap
    """
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


def plot_histogram_to_pixmap(hist_data: dict) -> QPixmap:
    """Строим гистограмму и возвращаем как QPixmap."""
    fig, ax = plt.subplots()
    xs = sorted(hist_data.keys())
    ys = [hist_data[x] for x in xs]
    ax.bar(xs, ys, width=1, color="blue")
    ax.set_title("Гистограмма амплитуд")
    ax.set_xlabel("Амплитуда") # Амплитуда от 0 до 255
    ax.set_ylabel("Частота") # Частота пикселей с определенной амплитудой

    # сохраняем в буфер
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)

    # превращаем в QPixmap
    buf.seek(0)
    qimg = QImage.fromData(buf.read(), "PNG")
    return QPixmap.fromImage(qimg)

def plot_correlation_estimation(corr_data):
    """Строим график оценки корреляционной функции"""
    fig, ax = plt.subplots()
    im = ax.imshow(corr_data, cmap='viridis')
    plt.title('Корреляционная функция')
    plt.colorbar(im, ax=ax)

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    plt.close(fig)

    # превращаем в QPixmap
    buf.seek(0)
    qimg = QImage.fromData(buf.read(), "PNG")
    return QPixmap.fromImage(qimg)

    # buf = BytesIO()
    # plt.savefig(buf, format='png', bbox_inches='tight')
    # plt.close(fig)
    # buf.seek(0)
    # img = Image.open(buf)
    # qimg = QPixmap.fromImage(ImageQt(img))