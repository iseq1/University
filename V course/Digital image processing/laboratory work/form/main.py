"""
Основная форма приложения
"""
from PyQt6.QtCore import Qt, pyqtSignal, QRect
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout,
    QPushButton, QFileDialog, QWidget,
    QDialog, QGridLayout, QHBoxLayout,
)
from core.first.image_transfer import LocalImageTransfer
from core.first.image_conventor import ByteConverter
from core.first.image_filter import Grayscale24Filter
from core.image_utils import array_to_pixmap
from numpy import copy, ndarray
from form.form_utils.roi_dialog_form import ROISelectionDialog
from form.form_utils.roi_form import ROIForm
from form.form_utils.roi_selecting import ROISelector


class MainWindow(QMainWindow):
    """Основная форма для взаимодействия с изображением"""

    mouse_moved = pyqtSignal(float, float)  # x, y координаты относительно QLabel

    def __init__(self):
        super().__init__()
        self.image_transfer = LocalImageTransfer()
        self.current_array = None  # Текущее изображение как NumPy-массив
        self.history = []  # Стек истории (для undo)
        self.setMouseTracking(True)  # Получение события без нажатия кнопок

        # UI
        self.label = ROISelector("Здесь будет ваше изображение")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.mouse_moved.connect(self.on_mouse_move)  # координаты пикселей
        self.label.roi_selected.connect(self.handle_roi_selection)  # выделение ROI
        self.status_label = QLabel("Статус: ничего не сделано")

        # кнопки
        self.btn_load = QPushButton("Загрузить")
        self.btn_save = QPushButton("Сохранить")
        self.btn_to_bytes = QPushButton("В байты")
        self.btn_from_bytes = QPushButton("Из байтов")
        self.btn_gray = QPushButton("В серый")
        self.btn_undo = QPushButton("Отмена")

        # левая часть (картинка + подписи)
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.label, stretch=5)
        left_layout.addWidget(self.status_label)

        # правая часть (кнопки в 2 колонки + одна посередине)
        right_layout = QGridLayout()

        # первая строка: загрузить / сохранить
        right_layout.addWidget(self.btn_load, 0, 0)
        right_layout.addWidget(self.btn_save, 0, 1)

        # вторая строка: в байты / из байтов
        right_layout.addWidget(self.btn_to_bytes, 1, 0)
        right_layout.addWidget(self.btn_from_bytes, 1, 1)

        # третья строка: кнопка по центру (занимает 2 колонки)
        right_layout.addWidget(self.btn_gray, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        # четвёртая строка: отмена по центру
        right_layout.addWidget(self.btn_undo, 3, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        right_layout.setRowStretch(0, 0)  # первая строка
        right_layout.setRowStretch(1, 0)  # вторая строка
        right_layout.setRowStretch(2, 0)  # третья строка
        right_layout.setRowStretch(3, 0)  # четвёртая строка
        right_layout.setRowStretch(4, 1)  # пятая "пустая" строка тянется и забирает всё место

        # общий layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=3)  # картинка + подписи
        main_layout.addLayout(right_layout, stretch=1)  # панель кнопок

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Handlers
        self.btn_load.clicked.connect(self.load_image)
        self.btn_save.clicked.connect(self.save_image)
        self.btn_gray.clicked.connect(self.apply_grayscale)
        self.btn_undo.clicked.connect(self.undo)
        self.btn_to_bytes.clicked.connect(self.convert_to_bytes)
        self.btn_from_bytes.clicked.connect(self.convert_from_bytes)
        self.mouse_moved.connect(self.on_mouse_move)

        # статусбар
        self.statusBar().showMessage("Координаты пикселя и RGB")

    def on_mouse_move(self, x, y) -> None:
        """
        Передача координат курсора на изображении

        :param x: координата по оси абсцисс
        :param y: координата по оси ординат
        :return: None
        """
        try:
            if isinstance(self.current_array, ndarray):
                h, w, _ = self.current_array.shape

                label_w = self.label.width()
                label_h = self.label.height()
                if label_w == 0 or label_h == 0:
                    return

                # координаты в исходном изображении
                x_img = int(x * w / label_w)
                y_img = int(y * h / label_h)

                if 0 <= x_img < w and 0 <= y_img < h:
                    r, g, b = self.current_array[y_img, x_img]
                    self.statusBar().showMessage(f"X: {x_img}, Y: {y_img} | R: {r}, G: {g}, B: {b}")
            elif isinstance(self.current_array, (bytes, bytearray)):
                self.statusBar().showMessage("Текущее состояние — массив байтов")
            else:
                self.statusBar().showMessage("Нет изображения")

        except Exception as e:
            print(f'Ошибка при отслеживании координат курсора: {e}')

    def handle_roi_selection(self, rect: QRect) -> None:
        """
        Обработчик выбора ROI на форме

        :param rect: Класс-представление прямоугольной плоскости
        :return: None
        """
        try:
            if self.current_array is None or not isinstance(self.current_array, ndarray):
                return

            # размеры QLabel и NumPy-изображения
            label_w, label_h = self.label.width(), self.label.height()
            img_h, img_w, _ = self.current_array.shape

            if label_w == 0 or label_h == 0:
                return

            # пересчёт координат из QLabel → в NumPy-массив
            scale_x = img_w / label_w
            scale_y = img_h / label_h

            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            x, y, w, h = int(x * scale_x), int(y * scale_y), int(w * scale_x), int(h * scale_y)

            # извлекаем ROI
            roi_array = self.current_array[y:y + h, x:x + w]

            if roi_array.size == 0:
                self.statusBar().showMessage("ROI пустой, выберите снова")
                return

            # превью ROI (QDialog)
            roi_pixmap = array_to_pixmap(roi_array)
            dialog = ROISelectionDialog(roi_pixmap, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # открываем отдельное окно с ROI
                self.roi_window = ROIForm(roi_array)
                self.roi_window.show()

        except Exception as e:
            print(f'Ошибка при выделении ROI на форме: {e}')

    def push_history(self) -> None:
        """Сохраняет копию текущего изображения в историю перед изменением."""

        try:
            if self.current_array is not None:
                if isinstance(self.current_array, ndarray):
                    # Bitmap
                    self.history.append(copy(self.current_array))
                elif isinstance(self.current_array, (bytes, bytearray)):
                    # bytes array
                    self.history.append(self.current_array[:])

        except Exception as e:
            print(f'Ошибка при добавлении в буфер в форме: {e}')

    def undo(self) -> None:
        """Отмена последнего действия (восстановление из истории)."""

        try:
            if not self.history:
                self.status_label.setText("Нет истории для \"Отмены\"")
                return
            self.current_array = self.history.pop()
            self.status_label.setText("Последнее действие отменено!")
            self.update_display()

        except Exception as e:
            print(f'Ошибка при отмене последнего действия в форме: {e}')

    def load_image(self):
        """Загрузка выбранного изображения в форму"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать изображение", "", "Images (*.png *.jpg *.bmp)")
            if file_path:
                self.current_array = self.image_transfer.load_image(file_path)
                self.history.clear()  # новая картинка — история сбрасывается
                self.status_label.setText("Изображение загружено в форму!")
                self.update_display()

        except Exception as e:
            print(f'Ошибка при загрузке изображения в форме: {e}')

    def save_image(self):
        """Сохранение обработанного изображения"""
        try:
            if self.current_array is None:
                self.status_label.setText("Невозможно сохранить изображение")
                return
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "",
                                                       "PNG (*.png);;JPEG (*.jpg *.jpeg)")
            if file_path:
                self.image_transfer.save_image(self.current_array, file_path)
                self.status_label.setText("Изображение сохранено!")

        except Exception as e:
            print(f'Ошибка при сохранении изображения на форме: {e}')

    def apply_grayscale(self):
        """Применение серого фильтра"""

        try:
            if self.current_array is None:
                self.status_label.setText("Нет изображения")
                return
            if isinstance(self.current_array, ndarray):
                # Bitmap
                self.push_history()  # сохраняем текущее состояние перед изменением
                filter = Grayscale24Filter(mode="bt601")
                self.current_array = filter.apply(self.current_array)
                self.status_label.setText("Изображение конвертировано в градациях серого!")
            self.update_display()

        except Exception as e:
            print(f'Ошибка при применении градации серого на форме: {e}')

    def convert_to_bytes(self):
        """Конвертируем текущее RGB-изображение в массив байтов (grayscale)."""

        try:
            convertor = ByteConverter()
            if self.current_array is not None:
                self.push_history()
                arr_bytes, msg = convertor.to_bytes(self.current_array)
                if arr_bytes is not None:
                    self.current_array = arr_bytes
                    self.status_label.setText(msg)
                else:
                    self.status_label.setText(msg)
                    return
            else:
                self.status_label.setText("Нет изображения")
                return

        except Exception as e:
            print(f'Ошибка при конвертации в массив байтов на форме: {e}')

    def convert_from_bytes(self):
        """Восстанавливаем изображение из массива байтов и отображаем в main_window."""

        try:
            if isinstance(self.current_array, (bytes, bytearray)):
                # ищем последнее состояние NumPy в истории
                for prev in reversed(self.history):
                    if isinstance(prev, ndarray):
                        h, w, _ = prev.shape
                        break
                else:
                    self.status_label.setText("Не найдено исходное изображение для размеров")
                    return

                convertor = ByteConverter()
                self.push_history()
                self.current_array, msg = convertor.from_bytes(self.current_array, h, w)
                self.status_label.setText(msg)
                self.update_display()

        except Exception as e:
            print(f'Ошибка при конвертации из массива байтов на форме: {e}')

    def update_display(self):
        """Обновляет QLabel с текущим изображением."""

        try:
            if isinstance(self.current_array, ndarray):
                # Bitmap
                pixmap = array_to_pixmap(self.current_array)
                self.label.setPixmap(
                    pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio,
                                  Qt.TransformationMode.SmoothTransformation)
                )
            elif isinstance(self.current_array, (bytes, bytearray)):
                # bytes array
                self.status_label.setText("Текущее состояние — массив байтов")

        except Exception as e:
            print(f'Ошибка при обновлении дисплея на форме: {e}')
