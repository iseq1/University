"""
Вспомогательная форма для реализации диалогового окна для работы с амплитудами пикселей
"""
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton
from form.form_utils.popup_form import PopupDialog


class PixelAmplitudeDialog(PopupDialog):
    def __init__(self, array, parent=None):
        super().__init__("Амплитуда пикселя", parent=parent)
        self.array = array
        self.result_array = array.copy()

        layout = PopupDialog.layout(self)

        # Ввод координат
        coord_layout = QHBoxLayout()
        coord_layout.addWidget(QLabel("X:"))
        self.x_input = QLineEdit()
        coord_layout.addWidget(self.x_input)
        coord_layout.addWidget(QLabel("Y:"))
        self.y_input = QLineEdit()
        coord_layout.addWidget(self.y_input)

        layout.addLayout(coord_layout)

        # Кнопка "Показать"
        self.btn_get = QPushButton("Показать амплитуду")
        self.btn_get.clicked.connect(self.show_amplitude)
        layout.addWidget(self.btn_get)

        # Показ амплитуд
        self.label_amp = QLabel("Амплитуда: —")
        layout.addWidget(self.label_amp)

        # Поле для новой амплитуды
        self.new_amp_input = QLineEdit()
        self.new_amp_input.setPlaceholderText("Новая амплитуда или R,G,B")
        layout.addWidget(self.new_amp_input)

        # Применить
        self.btn_apply = QPushButton("Изменить")
        self.btn_apply.clicked.connect(self.apply_change)
        layout.addWidget(self.btn_apply)

        # ОК
        btn_ok = QPushButton("Сохранить и выйти")
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)

    def get_result(self):
        return getattr(self, "result_array", None)

    def show_amplitude(self):
        """Демонстрация амплитуды пикселя"""
        from core.image_amplitude import ImageAmplitude
        x, y = int(self.x_input.text()), int(self.y_input.text())
        amp = ImageAmplitude.get_amplitude(self.array, x, y)
        if amp.get('data'):
            amplitude = amp['data']
            if isinstance(amplitude, int):
                self.label_amp.setText(f"Амплитуда в ({x}, {y}): {amplitude} | R: {amplitude}, G:{amplitude}, B:{amplitude}")
            elif isinstance(amplitude, tuple):
                R, G, B = amplitude
                amplitude = round((R+G+B)/3,1)
                self.label_amp.setText(f"Амплитуда в ({x}, {y}): {amplitude} | R: {R}, G:{G}, B:{B}")
            else:
                self.label_amp.setText("")
                raise ValueError("Некорректная передача амплитуды")
        else:
            self.label_amp.setText("")
            raise ValueError("Некорректный ответ от обработчика")

    def apply_change(self):
        """Изменение амплитуды пикселя"""
        try:
            from core.image_amplitude import ImageAmplitude, np

            x, y = int(self.x_input.text()), int(self.y_input.text())
            val = self.new_amp_input.text().strip()
            if ',' in val:
                new_value = np.array([int(v) for v in val.split(',')])
            else:
                new_value = int(val)
            request = ImageAmplitude.set_amplitude(self.result_array, x, y, new_value)
            if request.get('data', None) is not None:
                self.result_array = request['data']
            self.label_amp.setText(f"✅ Изменено: {new_value}")
        except Exception as e:
            self.label_amp.setText(f"Ошибка: {e}")
