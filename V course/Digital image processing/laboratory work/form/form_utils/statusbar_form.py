"""
Вспомогательная форма для реализации статус-бара
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QStatusBar, QFrame, QLabel, QWidget, QHBoxLayout, QVBoxLayout


class CustomStatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setLineWidth(1)
        separator.setMidLineWidth(0)

        # левые и правые блоки
        self.status_left = QLabel("")
        self.status_right = QLabel("")
        self.status_right.setAlignment(Qt.AlignmentFlag.AlignRight)

        # контейнер с layout
        container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.status_left, stretch=1)
        layout.addWidget(self.status_right, stretch=1)
        container.setLayout(layout)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(separator)
        main_layout.addWidget(container)
        main_widget.setLayout(main_layout)

        # добавляем в статусбар
        self.addPermanentWidget(main_widget, 1)

        self.setMouseTracking(True)