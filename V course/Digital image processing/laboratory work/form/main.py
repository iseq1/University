"""
Основная форма приложения
"""
from PyQt6.QtCore import Qt, pyqtSignal, QRect
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QFileDialog, QWidget,
    QDialog, QComboBox, QToolBar, QMessageBox, QPushButton, QMenu,
)

from core.image_correlation import ImageCorrelationHandler
from core.image_hist_computer import ImageHistogram
from core.image_linear_contrast import ImageLinearContrast
from core.image_noise import ImageDenoiseHandler
from core.image_piecewise_computer import ImagePiecewiseHandler
from core.image_rotate import ImageRotate
from core.image_scale import ImageScale
from core.image_smooth import ImageSmoothing
from core.image_stat_computer import ImageStats
from core.image_transfer import LocalImageTransfer
from core.image_conventor import ByteConverter
from core.image_filter import Grayscale24Filter
from core.image_utils import array_to_pixmap, plot_histogram_to_pixmap, plot_correlation_estimation
from numpy import copy, ndarray
import form.const as c
from form.form_utils.create_image_dialog_form import CreateImageDialog
from form.form_utils.popup_form import PopupDialog, PixelAmplitudeDialog
from form.form_utils.roi_dialog_form import ROISelectionDialog
from form.form_utils.roi_selecting import ROISelector
from form.form_utils.statusbar_form import CustomStatusBar
from core.logger import CustomLogger

logger = CustomLogger.get_logger()


class MainWindow(QMainWindow):
    """Основная форма для взаимодействия с изображением"""

    mouse_moved = pyqtSignal(float, float)  # Координаты (x, y) относительно QLabel

    def __init__(self):
        super().__init__()

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

        toolbar.addWidget(self.init_general_button())
        toolbar.addSeparator()
        toolbar.addWidget(self.init_image_button())
        toolbar.addSeparator()
        toolbar.addWidget(self.init_roi_button())
        toolbar.addSeparator()

    def init_general_button(self):
        """UI: общая кнопка формы"""
        btn = QPushButton("Общее")
        btn.setStyleSheet(c.BUTTON_STYLE)
        menu_gen = QMenu(self)

        for name, cfg in c.GENERAL_COMBO_MAP.items():
            if not cfg:
                continue

            t = cfg.get('type')

            if t == 'btn':
                menu_gen.addAction(name, lambda checked=False, n=name: self._gen_action_selected(n))
            elif t == 'menu':
                _menu = QMenu(name, self)
                menu_params = cfg.get('menu_params')

                items = menu_params.get('items', [])
                for item in items:
                    _menu.addAction(item['label'], lambda checked=False, f=item['action']: f(self))

                menu_gen.addMenu(_menu)

        btn.setMenu(menu_gen)
        return btn

    def init_image_button(self):
        """UI: кнопка взаимодействия с изображением"""
        image_btn = QPushButton("Изображение")
        image_btn.setStyleSheet(c.BUTTON_STYLE)
        menu_img = QMenu(self)

        for name, cfg in c.IMAGE_COMBO_MAP.items():
            if not cfg:
                continue

            t = cfg.get('type')

            if t == 'btn':
                menu_img.addAction(name, lambda checked=False, n=name: self._img_action_selected(n))
            elif t == 'menu':
                _menu = QMenu(name, self)
                menu_params = cfg.get('menu_params')

                items = menu_params.get('items', [])
                for item in items:
                    _menu.addAction(item['label'], lambda checked=False, f=item['action']: f(self))

                menu_img.addMenu(_menu)

        image_btn.setMenu(menu_img)
        return image_btn

    def init_roi_button(self):
        roi_btn = QPushButton("ROI")
        roi_btn.setStyleSheet(c.BUTTON_STYLE)
        menu_roi = QMenu(self)

        for name, cfg in c.ROI_COMBO_MAP.items():
            if not cfg:
                continue

            t = cfg.get('type')

            if t == 'btn':
                menu_roi.addAction(name, lambda checked=False, n=name: self._roi_action_selected(n))
            elif t == 'menu':
                _menu = QMenu(name, self)
                menu_params = cfg.get('menu_params')

                items = menu_params.get('items', [])
                for item in items:
                    _menu.addAction(item['label'], lambda checked=False, f=item['action']: f(self))

                menu_roi.addMenu(_menu)

        roi_btn.setMenu(menu_roi)
        return roi_btn

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

    def _gen_action_selected(self, action: str):
        """обработчик кнопок из комбо-бокса Общее"""
        try:
            cfg = c.GENERAL_COMBO_MAP.get(action, None)
            if not cfg:
                return

            action_func = cfg.get('action')
            if callable(action_func):
                action_func(self)
            else:
                raise TypeError(f"Для '{action}' не найдена корректная функция.")


        except Exception as e:
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

    def _img_action_selected(self, action: str):
        """Обработчик кнопок из комбо-бокса Изображения"""
        try:
            cfg = c.IMAGE_COMBO_MAP.get(action, None)
            if not cfg:
                return

            action_func = cfg.get('action')
            if callable(action_func):
                action_func(self)
            else:
                raise TypeError(f"Для '{action}' не найдена корректная функция.")


        except Exception as e:
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

    def _roi_action_selected(self, action):
        """Обработчик кнопок из комбо-бокса"""
        try:
            cfg = c.ROI_COMBO_MAP.get(action, None)
            if not cfg:
                return
            action_func = cfg.get('action')
            if callable(action_func):
                action_func(self)
            else:
                raise TypeError(f"Для '{action}' не найдена корректная функция.")

        except Exception as e:
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

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
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

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
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

    def clear_roi(self):
        """Очистка ROI"""
        try:
            self.current_roi_rect = None
            self.current_roi_array = None
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('clear_roi_corrected'))
            self.update_display()
        except Exception as e:
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

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
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

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
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

    def load_image(self):
        """Загрузка выбранного изображения в форму"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать изображение", "", "Images (*.png *.jpg *.bmp)")
            if file_path:
                self.current_array = LocalImageTransfer().load_image(file_path)
                self.history.clear()  # новая картинка — история сбрасывается
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('load_corrected'))
                self.update_display()
                CustomLogger.auto(logger, msg_map=c.LOGGER_MSG_MAP)

        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('load_failed'))
            CustomLogger.auto(
                logger=logger,
                msg_map=c.LOGGER_MSG_MAP,
                level="error",
                status="error",
                extra_msg=str(e)
            )

    def save_image(self):
        """Сохранение обработанного изображения"""
        try:
            if self.current_array is None:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('save_failed'))
                return

            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "",
                                                       "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp)")
            if file_path:
                LocalImageTransfer().save_image(self.current_array, file_path)
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('save_corrected'))
                CustomLogger.auto(logger, msg_map=c.LOGGER_MSG_MAP)

        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('save_failed'))
            CustomLogger.auto(
                logger=logger,
                msg_map=c.LOGGER_MSG_MAP,
                level="error",
                status="error",
                extra_msg=str(e)
            )

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
                CustomLogger.auto(logger, msg_map=c.LOGGER_MSG_MAP)

            self.update_display()

        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('grayscale_failed'))
            CustomLogger.auto(
                logger=logger,
                msg_map=c.LOGGER_MSG_MAP,
                level="error",
                status="error",
                extra_msg=str(e)
            )

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
                    CustomLogger.auto(logger, msg_map=c.LOGGER_MSG_MAP, extra_msg=msg)
                else:
                    self.statusbar.status_right.setText(msg)
                    CustomLogger.auto(logger,
                                      msg_map=c.LOGGER_MSG_MAP,
                                      level='warning',
                                      status='warning')
                    return
            else:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_image'))
                CustomLogger.auto(logger,
                                  msg_map=c.LOGGER_MSG_MAP,
                                  level='warning',
                                  status='warning')
                return

        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('convert_tb_failed'))
            CustomLogger.auto(
                logger=logger,
                msg_map=c.LOGGER_MSG_MAP,
                level="error",
                status="error",
                extra_msg=str(e)
            )

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
                    CustomLogger.auto(logger,
                                      msg_map=c.LOGGER_MSG_MAP,
                                      level='warning',
                                      status='warning')
                    return

                convertor = ByteConverter()
                self.push_history()
                self.current_array, msg = convertor.from_bytes(self.current_array, h, w)
                self.statusbar.status_right.setText(msg)
                self.update_display()
                CustomLogger.auto(logger, msg_map=c.LOGGER_MSG_MAP)

        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('convert_fb_failed'))
            CustomLogger.auto(
                logger=logger,
                msg_map=c.LOGGER_MSG_MAP,
                level="error",
                status="error",
                extra_msg=str(e)
            )

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
                    CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, extra_msg=str(msg))
                    popup.exec()

                if response.get('code'):
                    self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'get_{response["code"]}_corrected'))
            elif isinstance(self.current_array, (bytes, bytearray)):
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'no_update_display'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
            elif self.current_array is not None and self.current_roi_array is None:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_roi'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
            else:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_image'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('get_stat_failed'))
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

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
                    CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP)
                    popup.exec()
                if response.get('code'):
                    self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'get_{response["code"]}_corrected'))
            elif isinstance(self.current_array, (bytes, bytearray)):
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'no_update_display'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
            elif self.current_array is not None and self.current_roi_array is None:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_roi'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
            else:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_image'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('get_hist_failed'))
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

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
                    CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP)
                    popup.exec()
                if response.get('code'):
                    self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'get_{response["code"]}_corrected'))
            elif isinstance(self.current_array, (bytes, bytearray)):
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'no_update_display'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
            elif self.current_array is not None and self.current_roi_array is None:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_roi'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
            else:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_image'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('get_contrast_failed'))
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

    def compute_smooth(self, array, radius: int=3):
        """Обертка для получения сглаживания"""
        try:
            if isinstance(array, ndarray):
                response = ImageSmoothing.apply(array, radius=radius)
                if response.get("data", None) is not None:
                    msg, img = self.format_data(response)
                    popup = PopupDialog(title="Сглаженное изображение по R={}".format(radius),
                                        message=msg,
                                        pixmap=img,
                                        parent=self)
                    CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, extra_msg='R = {}'.format(radius))
                    popup.exec()
                if response.get('code'):
                    self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'get_{response["code"]}_corrected'))
            elif isinstance(self.current_array, (bytes, bytearray)):
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'no_update_display'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
            elif self.current_array is not None and self.current_roi_array is None:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_roi'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
            else:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_image'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('get_smooth_failed'))
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

    def compute_rotate(self, array, angle: float=90):
        """Обертка для поворота изображения"""
        try:
            if isinstance(array, ndarray):
                response = ImageRotate.apply(array, angle_deg=angle)
                if response.get("data", None) is not None:
                    self.push_history()
                    self.current_array = response["data"]

                    if self.current_roi_array is not None:
                        roi_response = ImageRotate.apply(self.current_roi_array, angle_deg=angle)
                        self.current_roi_array = roi_response["data"]
                        self.current_roi_rect = ImageRotate.rotate_roi_rect(self.current_roi_rect, array.shape, angle)

                    self.update_display()

                    CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, extra_msg='Угол поворота = {}'.format(angle))
                if response.get('code'):
                    self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'get_{response["code"]}_corrected'))
            elif isinstance(self.current_array, (bytes, bytearray)):
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'no_update_display'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
            else:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_image'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('get_rotate_failed'))
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

    def compute_scale(self, array, scale_x: float, scale_y: float, method: str):
        """Обертка для масштабирования изображения"""
        try:
            if isinstance(array, ndarray):
                response = ImageScale.apply(array, scale_x=scale_x, scale_y=scale_y, method=method)
                if response.get("data", None) is not None:
                    self.push_history()
                    old_shape = self.current_array.shape
                    self.current_array = response["data"]

                    if self.current_roi_array is not None:
                        roi_response = ImageScale.apply(self.current_roi_array, scale_x=scale_x, scale_y=scale_y, method=method)
                        self.current_roi_array = roi_response["data"]
                        self.current_roi_rect = ImageScale.scale_roi_rect(self.current_roi_rect, scale_x, scale_y)

                    self.update_display()
                    mthd = 'Выборки' if method == 'nearest' else 'Интерполяции'
                    CustomLogger.auto(logger=logger,
                                      msg_map=c.LOGGER_MSG_MAP,
                                      extra_msg='Масштабирование методом "{mthd}" x{scale}\n'
                                                'Размеры до: {old_shape}\n'
                                                'Размеры после: {new_shape}'.format(mthd=mthd,
                                                                                    scale=scale_x,
                                                                                    old_shape=old_shape,
                                                                                    new_shape=self.current_array.shape))
                if response.get('code'):
                    self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'get_{response["code"]}_corrected'))
            elif isinstance(self.current_array, (bytes, bytearray)):
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'no_update_display'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
            else:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_image'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('get_scale_failed'))
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

    def compute_denoise(self, array):
        """Обертка для уменьшения уровня белого аддитивного шума"""
        try:
            if isinstance(array, ndarray):
                response = ImageDenoiseHandler.apply(array)
                if response.get("data", None) is not None:
                    msg, img = self.format_data(response)
                    popup = PopupDialog(title="Изображение с уменьшенным шумом", message=msg, pixmap=img, parent=self)
                    CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, extra_msg=f'{response["msg"]}')
                    popup.exec()
                if response.get('code'):
                    self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'get_{response["code"]}_corrected'))
            elif isinstance(self.current_array, (bytes, bytearray)):
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'no_update_display'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
            elif self.current_array is not None and self.current_roi_array is None:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_roi'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
            else:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_image'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('get_noise_failed'))
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

    def compute_amplitude(self, array):
        """Обертка для взаимодействия с амплитудой пикселей"""
        try:
            if isinstance(array, ndarray):
                dialog = PixelAmplitudeDialog(array, self)
                if dialog.exec()  == QDialog.DialogCode.Accepted:
                    self.push_history()
                    result = dialog.get_result()
                    if result is not None:
                        self.current_array = result

                        if self.current_roi_array is not None:
                            x, y, w, h = self.current_roi_rect
                            self.current_roi_array = self.current_array[y:y + h, x:x + w].copy()

                    self.update_display()
                    CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP)
                    self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'get_amplitude_corrected'))

            elif isinstance(self.current_array, (bytes, bytearray)):
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'no_update_display'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
            else:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_image'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('get_amplitude_failed'))
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

    def compute_piecewise(self, array, block_size: int):
        """Обертка для масштабирования изображения"""
        try:
            if isinstance(array, ndarray):
                response = ImagePiecewiseHandler.apply(array, block_size)
                if response.get("data", None) is not None:
                    msg, img = self.format_data(response)
                    popup = PopupDialog(title="Карта изображения с блоками={}x{}".format(block_size, block_size),
                                        message=msg,
                                        pixmap=img,
                                        parent=self)
                    CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, extra_msg='Блок = {}x{}'.format(block_size, block_size))
                    popup.exec()
                if response.get('code'):
                    self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'get_{response["code"]}_corrected'))
            elif isinstance(self.current_array, (bytes, bytearray)):
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'no_update_display'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
            else:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_image'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('get_piecewise_failed'))
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

    def compute_mia(self, mode: str):
        """Обертка для построения изображения сцены с взаимно независимыми амплитудами"""
        try:
            dialog = CreateImageDialog(mode, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.push_history()
                result = dialog.get_result()
                msg = dialog.get_msg()
                if result is not None:
                    self.current_array = result

                    if self.current_roi_array is not None:
                        x, y, w, h = self.current_roi_rect
                        self.current_roi_array = self.current_array[y:y + h, x:x + w].copy()

                self.update_display()
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, extra_msg=msg)
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'get_{str(mode)}_corrected'))

        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'get_{str(mode)}_failed'))
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

    def compute_correlation(self, array):
        """Обертка для оценки корреляционной функции"""
        try:
            if isinstance(array, ndarray):
                response = ImageCorrelationHandler.apply(array)
                if response.get('data', None) is not None:
                    msg, img = self.format_data(response)
                    popup = PopupDialog(title="Оценка корреляционной функции", message=msg, pixmap=img, parent=self)
                    CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP)
                    popup.exec()
                if response.get('code'):
                    self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'get_{response["code"]}_corrected'))
            elif isinstance(self.current_array, (bytes, bytearray)):
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get(f'no_update_display'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')
            else:
                self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('no_image'))
                CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='warning', level='warning')

        except Exception as e:
            self.statusbar.status_right.setText(c.STATUS_BAR_MSG.get('get_correlation_failed'))
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

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
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))

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

    def format_smooth_img(self, smooth):
        """
        Форматирование информации для вывода сглаженного изображения
        :param smooth:
        :return:
        """
        text = None
        img = array_to_pixmap(smooth) if smooth is not None else None

        return text, img

    def format_piecewise_img(self, piecewise):
        """
        Форматирование информации для вывода карты изображения
        :param piecewise:
        :return:
        """
        text = None
        img = array_to_pixmap(piecewise) if piecewise is not None else None

        return text, img

    def format_correlation_img(self, correlation):
        """
        Форматирование информации для вывода оценки корреляционной функции
        :param correlation:
        :return:
        """
        text = None
        img = plot_correlation_estimation(correlation) if correlation is not None else None

        return text, img

    def format_denoise_img(self, denoise):
        """
        Форматирование информации для вывода бесшумного изображения
        :param denoise:
        :return:
        """
        text = None
        img = array_to_pixmap(denoise) if denoise is not None else None

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
            CustomLogger.auto(logger=logger, msg_map=c.LOGGER_MSG_MAP, status='error', level='error', extra_msg=str(e))