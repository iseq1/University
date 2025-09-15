from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout


class ROISelectionDialog(QDialog):
    def __init__(self, roi_pixmap, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Предпросмотр ROI")

        self.label = QLabel()
        self.label.setPixmap(roi_pixmap)

        btn_ok = QPushButton("Утвердить")
        btn_cancel = QPushButton("Отмена")
        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(btn_ok)
        layout.addWidget(btn_cancel)
        self.setLayout(layout)