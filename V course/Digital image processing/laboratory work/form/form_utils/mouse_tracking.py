from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QLabel


class MouseTracker(QLabel):
    mouse_moved = pyqtSignal(float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        pos = event.position()
        self.mouse_moved.emit(pos.x(), pos.y())
        super().mouseMoveEvent(event)

    def enterEvent(self, event):
        """Когда мышь заходит в область изображения — ставим крестик."""
        self.setCursor(Qt.CursorShape.CrossCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Когда мышь выходит — возвращаем обычный курсор."""
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)



