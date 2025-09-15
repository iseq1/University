from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from core.image_utils import array_to_pixmap


class ROIForm(QWidget):
    def __init__(self, roi_array, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Работа с ROI")
        self.label = QLabel()
        self.label.setPixmap(array_to_pixmap(roi_array))

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)