"""
Основная форма приложения
"""
from PyQt6.QtCore import Qt, pyqtSignal, QRect
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QFileDialog, QWidget,
    QDialog, QComboBox, QToolBar, QMessageBox,
)

from core.image_hist_computer import ImageHistogram
from core.image_linear_contrast import ImageLinearContrast
from core.image_stat_computer import ImageStats
from core.image_transfer import LocalImageTransfer
from core.image_conventor import ByteConverter
from core.image_filter import Grayscale24Filter
from core.image_utils import array_to_pixmap, plot_histogram_to_pixmap
from numpy import copy, ndarray
import form.const as c
from form.form_utils.popup_form import PopupDialog
from form.form_utils.roi_dialog_form import ROISelectionDialog
from form.form_utils.roi_selecting import ROISelector
from form.form_utils.statusbar_form import CustomStatusBar


class MainWindow(QMainWindow):
    """Основная форма для взаимодействия с изображением"""

    mouse_moved = pyqtSignal(float, float)  # Координаты (x, y) относительно QLabel

    def __init__(self):
        super().__init__()

        self.image_transfer = LocalImageTransfer() # Взаимодействие с медиа-файлами
        self.setMouseTracking(True)  # Отслеживание действий курсора
        self.mouse_moved.connect(self.on_mouse_move) # Обработчик местоположения курсора
        self.current_array = None  # Изображение (NumPy-массив)
        self.current_roi_array = None  # ROI (NumPy-массив)
        self.current_roi_rect = None  # координаты ROI в системе исходного массива (x, y, w, h)
        self.history = []  # Стек истории
        self.init_ui() # Пользовательский интерфейс

    def resizeEvent(self, event):
        """Автоматическое масштабирование"""
        self.update_display()
        super().resizeEvent(event)

    def init_toolbar(self):
        """ UI: Главное панель взаимодействия """

        toolbar = QToolBar("Главная панель")
        self.addToolBar(toolbar)

        # Кнопки
        self.image_combo = QComboBox()
        self.image_combo.addItems(c.IMAGE_COMBO_MAP.keys())
        self.image_combo.currentTextChanged.connect(self._img_action_selected)
        toolbar.addWidget(self.image_combo)

        toolbar.addSeparator()

        # Комбо-бокс с кнопками
        self.roi_combo = QComboBox()
        self.roi_combo.addItems(c.ROI_COMBO_MAP.keys())
        self.roi_combo.currentTextChanged.connect(self._roi_action_selected)
        toolbar.addWidget(self.roi_combo)

        toolbar.addSeparator()
        toolbar.addAction("Отменить", self.undo)
        toolbar.addSeparator()

    def init_statusbar(self):
        """ UI: Панель статусов """
        self.statusbar = CustomStatusBar(self)
        self.setStatusBar(self.statusbar)

    def init_label(self):
        """ UI: Лейбл под изображение """
        self.label = ROISelector("Здесь будет ваше изображение")
        self.label.setScaledContents(False)  # пусть скейлим сами
        self.label.setMinimumSize(200, 200)  # чтобы не схлопывалась
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.mouse_moved.connect(self.on_mouse_move)  # координаты пикселей
        self.label.roi_selected.connect(self.handle_roi_selection)  # выделение ROI

    def init_ui(self):
        """ UI: Сборка полного пользовательского интерфейса """
        self.init_toolbar()
        self.init_statusbar()
        self.init_label()

        layout = QVBoxLayout()
        layout.addWidget(self.label, stretch=5)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _img_action_selected(self, action: str):
        """Обработчик кнопок из комбо-бокса Изображения"""
        try:
            func = c.IMAGE_COMBO_MAP.get(action, None)
            if func is not None:
                func(self)
            self.image_combo.setCurrentIndex(0)

        except Exception as e:
            print(f'Ошибка при выборе действия над изображением: {e}')

    def _roi_action_selected(self, action):
        """Обработчик кнопок из комбо-бокса"""
        try:
            func = c.ROI_COMBO_MAP.get(action, None)
            if func is not None:
                func(self)
            self.roi_combo.setCurrentIndex(0)

        except Exception as e:
            print(f'Ошибка при выборе действия над ROI: {e}')

    def on_mouse_move(self, x, y) -> None:
        """
        Передача координат курсора на изображении

        :param x: координата по оси абсцисс
        :param y: координата по оси ординат
        :return: None
        """
        try:

            if isinstance(self.current_array, ndarray):
                pixmap = self.label.pixmap()
                if pixmap is None:
                    return

                # размеры оригинального массива
                h, w, _ = self.current_array.shape

                # размеры отмасштабированного изображения (на экране)
                scaled_w, scaled_h = pixmap.width(), pixmap.height()

                # размеры QLabel
                label_w, label_h = self.label.width(), self.label.height()

                # пересчёт координат курсора → в исходное изображение
                x_img = int((x) * w / scaled_w)
                y_img = int((y) * h / scaled_h)

                if 0 <= x_img < w and 0 <= y_img < h:
                    r, g, b = self.current_array[y_img, x_img]
                    amp = round((int(r) + int(g) + int(b)) / 3, 1)

                    # выводим значения в кастомный статусбар
                    self.statusbar.status_left.setText(f"X: {x_img}, Y: {y_img} | "
                                                       f"R: {r}, G: {g}, B: {b} | "
                                                       f"Amplitude: {amp}")


            elif isinstance(self.current_array, (bytes, bytearray)):
                self.statusbar.status_left.setText(c.STATUS_BAR_MSG.get('no_update_display'))
            else:
                self.statusbar.status_left.setText(c.STATUS_BAR_MSG.get('no_image'))
        except Exception as e:
            print(f'Ошибка при отслеживании координат курсора: {e}')

    def handle_roi_selection(self, rect: QRect) -> None:
        """
        Обработчик выбора ROI на форме

        :param rect: Класс-представление прямоугольной плоскости
        :return: None
        """
        try:
            # Проверка на корректное наличие изображения на форме
            if self.current_array is None or not isinstance(self.current_array, ndarray):
                return

            # Размеры исходного изображения
            img_h, img_w, _ = self.current_array.shape

            # Проверка отображения текущего изображения
            pixmap = self.label.pixmap()
            if pixmap is None:
                return

            # Размеры текущего изображения
            scaled_w, scaled_h = pixmap.width(), pixmap.height()
            label_w, label_h = self.label.width(), self.label.height()

            # Смещение для центрирования
            offset_x = (label_w - scaled_w) // 2
            offset_y = (label_h - scaled_h) // 2

            # Вычисление координат ROI с учетом масштабирования изображения
            x, y, w, h = max(rect.x() - offset_x, 0), max(rect.y() - offset_y, 0), rect.width(), rect.height() # Коорд.

            scale_x = img_w / scaled_w # Коэф. масштабирования по Х
            scale_y = img_h / scaled_h # Коэф. Масштабирования по Y

            x_img, y_img, w_img, h_img = int(x * scale_x), int(y * scale_y), int(w * scale_x), int(h * scale_y) # Масштаб.

            x_img, y_img = max(0, min(x_img, img_w - 1)), max(0, min(y_img, img_h - 1)) #
            w_img, h_img = min(w_img, img_w - x_img), min(h_img, img_h - y_img) #

            roi_array = self.current_array[y_img:y_img + h_img, x_img:x_img + w_img]
            if roi_array.size == 0:
                self.statusbar.status_left.setText("ROI пустой, выберите снова")
                return

            self.current_roi_rect = (x_img, y_img, w_img, h_img)
            self.current_roi_array = roi_array

            # отобразим подтверждение
            roi_pixmap = array_to_pixmap(self.current_roi_array)
            dialog = ROISelectionDialog(roi_pixmap, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('set_roi_corrected'))
                self.update_display()  # перерисовать с ROI
            else:
                self.clear_roi()


        except Exception as e:
            print(f'Ошибка при выделении ROI на форме: {e}')

    def clear_roi(self):
        """Очистка ROI"""
        try:
            self.current_roi_rect = None
            self.current_roi_array = None
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('clear_roi_corrected'))
            self.update_display()
        except Exception as e:
            print(f"Ошибка при очистке ROI: {e}")

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
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('undo_failed'))
                return
            self.current_array = self.history.pop()
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('undo_corrected'))
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
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('load_corrected'))
                self.update_display()

        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('load_failed'))
            print(f'Ошибка при загрузке изображения в форме: {e}')

    def save_image(self):
        """Сохранение обработанного изображения"""
        try:
            if self.current_array is None:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('save_failed'))

                return
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "",
                                                       "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp)")
            if file_path:
                self.image_transfer.save_image(self.current_array, file_path)
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('save_corrected'))

        except Exception as e:
            print(f'Ошибка при сохранении изображения на форме: {e}')

    def apply_grayscale(self):
        """Применение серого фильтра"""

        try:
            if self.current_array is None:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_image'))

                return
            if isinstance(self.current_array, ndarray):
                # Bitmap
                self.push_history()  # сохраняем текущее состояние перед изменением
                filter = Grayscale24Filter(mode="bt601")
                self.current_array = filter.apply(self.current_array)
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('grayscale_corrected'))

            self.update_display()

        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('grayscale_failed'))
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
                    self.statusbar.status_right.setText(msg)
                else:
                    self.statusbar.status_right.setText(msg)
                    return
            else:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_image'))
                return

        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('convert_tb_failed'))
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
                    self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_image'))
                    return

                convertor = ByteConverter()
                self.push_history()
                self.current_array, msg = convertor.from_bytes(self.current_array, h, w)
                self.statusbar.status_right.setText(msg)
                self.update_display()

        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('convert_fb_failed'))
            print(f'Ошибка при конвертации из массива байтов на форме: {e}')

    def compute_stats(self, array, border_only=False):
        """Обёртка для вызова расчёта статистики."""
        try:
            if isinstance(array, ndarray):
                response = ImageStats.compute(array, border_only=border_only)
                if response.get('data'):
                    msg, img = self.format_data(response)
                    popup = PopupDialog(title="Статистика изображения",
                                        message=msg,
                                        pixmap=img,
                                        parent=self)
                    popup.exec()

                if response.get('code'):
                    self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'get_{response['code']}_corrected'))
            elif isinstance(self.current_array, (bytes, bytearray)):
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'no_update_display'))
            elif self.current_array is not None and self.current_roi_array is None:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_roi'))
            else:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_image'))
        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('get_stat_failed'))
            print(f'Ошибка при расчёте статистики изображении: {e}')

    def compute_hist(self, array, border_only=False):
        """Обёртка для построения гистограммы."""
        try:
            if isinstance(array, ndarray):
                response = ImageHistogram.compute(array, border_only=border_only)
                if response.get("data"):
                    msg, img = self.format_data(response)
                    popup = PopupDialog(title="Гистограмма изображения",
                                        message=msg,
                                        pixmap=img,
                                        parent=self)
                    popup.exec()
                if response.get('code'):
                    self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'get_{response['code']}_corrected'))
            elif isinstance(self.current_array, (bytes, bytearray)):
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'no_update_display'))
            elif self.current_array is not None and self.current_roi_array is None:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_roi'))
            else:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_image'))
        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('get_hist_failed'))
            print(f"Ошибка при построении гистограммы: {e}")

    def compute_contrast(self, array):
        """Обёртка для рассчитывания контраста"""
        try:
            if isinstance(array, ndarray):
                response = ImageLinearContrast.apply(array)
                if response.get("data", None) is not None:
                    msg, img = self.format_data(response)
                    popup = PopupDialog(title="Контрастное изображения",
                                        message=msg,
                                        pixmap=img,
                                        parent=self)
                    popup.exec()
                if response.get('code'):
                    self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'get_{response['code']}_corrected'))
            elif isinstance(self.current_array, (bytes, bytearray)):
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'no_update_display'))
            elif self.current_array is not None and self.current_roi_array is None:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_roi'))
            else:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_image'))
        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('get_contrast_failed'))
            print(f"Ошибка при построении контрастного изображения: {e}")


    def format_data(self, data: dict):
        """
        Форматирование полученных данных для последующей демонстрации
        :param data: словарь с рассчитанными значениями
        :param title: заголовок окна
        """
        try:
            code = data.get('code')
            func = c.FORMAT_DATA_MAP.get(code, None)
            if func is not None:
                return func(self, data.get('data'))

        except Exception as e:
            print(f'Ошибка при демонстрации PopUp статистики: {e}')

    def format_stat_img(self, stats: dict):
        """
        Форматирование информации для вывода статистики изображения
        :param stats: Рассчитанная статистика
        :return: Текст сообщения и сопроводительное изображение
        """
        text = (
            f"{'Минимальное значение:':30} {stats.get('min')}\n"
            f"{'Максимальное значение:':30} {stats.get('max')}\n"
            f"{'Выборочное среднее:':30} {stats.get('mean'):.2f}\n"
            f"{'Стандартное отклонение:':30} {stats.get('std'):.2f}"
        )
        img = None
        return text, img

    def format_hist_img(self, hist: dict):
        """
        Форматирование информации для вывода гистограммы изображения
        :param hist: Рассчитанная гистограмма
        :return: Текст сообщения и сопроводительное изображение
        """
        text = None
        img = plot_histogram_to_pixmap(hist)
        return text, img

    def format_contrast_img(self, contrast):
        """
        Форматирование информации для вывода линейного контрастированного изображения
        :param contrast:
        :return:
        """
        text = None
        img = array_to_pixmap(contrast) if contrast is not None else None

        return text, img

    def update_display(self):
        """Обновляет QLabel с текущим изображением."""

        try:
            if isinstance(self.current_array, ndarray):
                # Bitmap
                pixmap = array_to_pixmap(self.current_array)
                # масштабируем под размеры QLabel
                label_w = self.label.width()
                label_h = self.label.height()
                if label_w > 0 and label_h > 0:
                    scaled_pixmap = pixmap.scaled(
                        label_w, label_h,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )

                    if self.current_roi_rect:
                        img_h, img_w, _ = self.current_array.shape
                        x_img, y_img, w_img, h_img = self.current_roi_rect

                        # переводим ROI из координат изображения → в координаты scaled_pixmap
                        roi_rect = QRect(
                            int(x_img * scaled_pixmap.width() / img_w),
                            int(y_img * scaled_pixmap.height() / img_h),
                            int(w_img * scaled_pixmap.width() / img_w),
                            int(h_img * scaled_pixmap.height() / img_h),
                        )

                        painter = QPainter(scaled_pixmap)
                        painter.setPen(QPen(Qt.GlobalColor.green, 2, Qt.PenStyle.DashLine))
                        painter.drawRect(roi_rect)
                        painter.end()

                    self.label.setPixmap(scaled_pixmap)

            elif isinstance(self.current_array, (bytes, bytearray)):
                self.statusbar.status_left.setText(c.STATUS_BAR_MSG.get('no_update_display'))

        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('update_display_failed'))
            print(f'Ошибка при обновлении дисплея на форме: {e}')