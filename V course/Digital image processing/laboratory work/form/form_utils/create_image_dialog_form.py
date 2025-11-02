from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox

from form.const import CREATE_IMAGE_MODE
from form.form_utils.popup_form import PopupDialog


class CreateImageDialog(PopupDialog):
    def __init__(self, array, mode, parent=None):
        super().__init__("Сгенерировать изображение", parent=parent)
        self.array = array
        self.result_array = array.copy()

        layout = PopupDialog.layout(self)

        if CREATE_IMAGE_MODE.get(mode, None) is not None:
            action_func = CREATE_IMAGE_MODE.get(mode)
            if callable(action_func):
                action_func(self, layout)
        else:
            pass

        self.setMinimumWidth(400)


    def inti_mia_img_ui(self, layout):
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
        # self.btn_generate.clicked.connect(self.generate_image)
        layout.addWidget(self.btn_generate)

        # Кнопка OK
        self.btn_ok = QPushButton("Сохранить и выйти")
        # self.btn_ok.clicked.connect(self._on_accept)
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