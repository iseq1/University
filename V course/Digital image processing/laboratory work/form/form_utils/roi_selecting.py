from PyQt6.QtCore import pyqtSignal, QRect, Qt
from PyQt6.QtGui import QPainter, QPen

from form.form_utils.mouse_tracking import MouseTracker


class ROISelector(MouseTracker):
    roi_selected = pyqtSignal(QRect)  # сигнал, когда выделили область

    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_pos = None
        self.end_pos = None
        self.drawing = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_pos = event.pos()
            self.end_pos = self.start_pos
            self.drawing = True
            self.update()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end_pos = event.pos()
            self.update()
        super().mouseMoveEvent(event)  # важно, чтобы сигнал mouse_moved из ImageLabel продолжал работать

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            rect = QRect(self.start_pos, self.end_pos).normalized()
            self.roi_selected.emit(rect)
            self.update()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.start_pos and self.end_pos and self.drawing:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.GlobalColor.red, 2, Qt.PenStyle.DashLine))
            rect = QRect(self.start_pos, self.end_pos)
            painter.drawRect(rect)