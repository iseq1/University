"""
Вспомогательна форма для реализации универсального PopUp инструмента
"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QScrollArea
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class PopupDialog(QDialog):
    """Универсальный попап для текста, картинок и статистики."""

    def __init__(self, title: str, message: str = "", pixmap: QPixmap = None, parent=None, editable: bool=False):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.pixmap = pixmap
        self.setMinimumSize(800, 450)

        layout = QVBoxLayout(self)

        # Текст
        if message:
            if editable:
                self.text_widget = QTextEdit()
                self.text_widget.setText(message)
                layout.addWidget(self.text_widget)
            else:
                self.text_widget = QLabel(message)
                self.text_widget.setTextInteractionFlags(
                    self.text_widget.textInteractionFlags()
                    | Qt.TextInteractionFlag.TextSelectableByMouse
                )
                self.text_widget.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
                layout.addWidget(self.text_widget)

        # Картинка
        if pixmap:
            img_label = QLabel()
            img_label.setPixmap(pixmap.scaledToWidth(800, Qt.TransformationMode.SmoothTransformation))
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(img_label)
            layout.addWidget(scroll_area)

            btn_save = QPushButton("Сохранить")
            btn_save.clicked.connect(self.save_img)
            layout.addWidget(btn_save)

        # Кнопка OK
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)

    def get_text(self) -> str:
        """Возвращает текст (если editable=True)."""
        if isinstance(self.text_widget, QTextEdit):
            return self.text_widget.toPlainText()
        return ""

    def save_img(self):
        """Сохраняем картинку из попапа."""
        if not self.pixmap:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить изображение",
            "",
            "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp)"
        )
        if file_path:
            self.pixmap.save(file_path)