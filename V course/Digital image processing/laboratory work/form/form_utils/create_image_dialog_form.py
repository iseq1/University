from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox

from core.image_random_creator import ImageRandomHandler, ImageSmoothingHandler
from form.const import CREATE_IMAGE_MODE
from form.form_utils.popup_form import PopupDialog


class CreateImageDialog(PopupDialog):
    def __init__(self, mode, parent=None):
        super().__init__("Сгенерировать изображение", parent=parent)
        self.result_array = None
        self.msg = None
        layout = PopupDialog.layout(self)

        if CREATE_IMAGE_MODE.get(mode, None) is not None:
            action_func = CREATE_IMAGE_MODE.get(mode)
            if callable(action_func):
                action_func(self, layout)
        else:
            pass

        self.setMinimumWidth(400)


    def init_mia_img_ui(self, layout):
        """Пользовательский интерфейс для создания изображения с взаимно независимыми амплитудами"""
        # Размеры изображения
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Ширина (w):"))
        self.w_input = QLineEdit("256")
        size_layout.addWidget(self.w_input)
        size_layout.addWidget(QLabel("Высота (h):"))
        self.h_input = QLineEdit("256")
        size_layout.addWidget(self.h_input)
        layout.addLayout(size_layout)

        # Тип распределения
        dist_layout = QHBoxLayout()
        dist_layout.addWidget(QLabel("Тип распределения:"))
        self.dist_combo = QComboBox()
        self.dist_combo.addItems(["Равномерное", "Нормальное"])
        self.dist_combo.currentTextChanged.connect(self._mia_update_param_fields)
        dist_layout.addWidget(self.dist_combo)
        layout.addLayout(dist_layout)

        # Параметры распределения (динамически)
        self.param_layout = QHBoxLayout()
        self.param1_label = QLabel("a:")
        self.param1_input = QLineEdit("0")
        self.param2_label = QLabel("b:")
        self.param2_input = QLineEdit("255")
        self.param_layout.addWidget(self.param1_label)
        self.param_layout.addWidget(self.param1_input)
        self.param_layout.addWidget(self.param2_label)
        self.param_layout.addWidget(self.param2_input)
        layout.addLayout(self.param_layout)

        # Кнопка "Сгенерировать"
        self.btn_generate = QPushButton("Сгенерировать изображение")
        self.btn_generate.clicked.connect(self.generate_mia)
        layout.addWidget(self.btn_generate)

        # Кнопка OK
        self.btn_ok = QPushButton("Сохранить и выйти")
        self.btn_ok.clicked.connect(self._on_accept)
        layout.addWidget(self.btn_ok)

    def init_smoothed_mia_img_ui(self, layout):
        """Пользовательский интерфейс для создания изображения методом скользящего суммирования по квадратной окрестности с радиусом R"""
        # Размеры изображения
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Ширина (w):"))
        self.w_input = QLineEdit("256")
        size_layout.addWidget(self.w_input)
        size_layout.addWidget(QLabel("Высота (h):"))
        self.h_input = QLineEdit("256")
        size_layout.addWidget(self.h_input)
        layout.addLayout(size_layout)

        # Тип распределения
        dist_layout = QHBoxLayout()
        dist_layout.addWidget(QLabel("Тип распределения: Нормальное"))
        layout.addLayout(dist_layout)

        # Параметры распределения (динамически)
        self.param_layout = QHBoxLayout()
        self.param1_label = QLabel("m:")
        self.param1_input = QLineEdit("128")
        self.param2_label = QLabel("σ:")
        self.param2_input = QLineEdit("20")
        self.param3_label = QLabel("r:")
        self.param3_input = QLineEdit("3")
        self.param_layout.addWidget(self.param1_label)
        self.param_layout.addWidget(self.param1_input)
        self.param_layout.addWidget(self.param2_label)
        self.param_layout.addWidget(self.param2_input)
        self.param_layout.addWidget(self.param3_label)
        self.param_layout.addWidget(self.param3_input)
        layout.addLayout(self.param_layout)

        # Кнопка "Сгенерировать"
        self.btn_generate = QPushButton("Сгенерировать изображение")
        self.btn_generate.clicked.connect(self.generate_smoothed_mia)
        layout.addWidget(self.btn_generate)

        # Кнопка OK
        self.btn_ok = QPushButton("Сохранить и выйти")
        self.btn_ok.clicked.connect(self._on_accept)
        layout.addWidget(self.btn_ok)


    def _mia_update_param_fields(self):
        """Меняет подписи под параметры при смене типа распределения"""
        dist_type = self.dist_combo.currentText()
        if dist_type == "Равномерное":
            self.param1_label.setText("a:")
            self.param2_label.setText("b:")
            self.param1_input.setText("0")
            self.param2_input.setText("255")
        else:
            self.param1_label.setText("m:")
            self.param2_label.setText("σ:")
            self.param1_input.setText("128")
            self.param2_input.setText("20")

    def generate_mia(self):
        try:
            new_h = int(self.h_input.text())
            new_w = int(self.w_input.text())
            new_dist_type = 'uniform' if self.dist_combo.currentText() == 'Равномерное' else 'normal'
            params = {
                'a': int(self.param1_input.text()),
                'b': int(self.param2_input.text()),
                'm': int(self.param1_input.text()),
                'sigma': int(self.param2_input.text()),
            }
            request = ImageRandomHandler.apply(h=new_h, w=new_w, dist_type=new_dist_type, params=params)
            self.result_array = request.get('data', None)
        except Exception as e:
            print(e)

    def generate_smoothed_mia(self):
        try:
            new_h = int(self.h_input.text())
            new_w = int(self.w_input.text())
            params = {
                'base': {
                    'm': int(self.param1_input.text()),
                    'sigma': int(self.param2_input.text()),
                },
                'radius': int(self.param3_input.text()),
            }

            request = ImageSmoothingHandler.apply(h=new_h, w=new_w, dist_type='normal', params=params)
            self.result_array = request.get('data', None)
            self.msg = request.get('msg', None)
        except Exception as e:
            print(e)

    def _on_accept(self):
        """Закрывает форму, если изображение готово"""
        if self.result_array is None:
            QMessageBox.warning(self, "Нет данных", "Сначала сгенерируйте изображение!")
            return
        self.accept()

    def get_result(self):
        return getattr(self, "result_array", None)

    def get_msg(self):
        return getattr(self, "msg", None)