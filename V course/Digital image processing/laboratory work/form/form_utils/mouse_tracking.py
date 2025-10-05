"""
Вспомогательная форма для отслеживания движения курсора мыши
"""
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QLabel


class MouseTracker(QLabel):
    """Форма для отслеживания движения курсора мыши"""
    mouse_moved = pyqtSignal(float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        """Обработчик движения курсора мыши"""

        pos = event.position()
        # получаем реальный pixmap
        pixmap = self.pixmap()
        if pixmap:
            scaled_w = pixmap.width()
            scaled_h = pixmap.height()
            label_w = self.width()
            label_h = self.height()

            offset_x = (label_w - scaled_w) // 2
            offset_y = (label_h - scaled_h) // 2

            # проверяем, попадает ли курсор в реальную область изображения
            if offset_x <= pos.x() <= offset_x + scaled_w and offset_y <= pos.y() <= offset_y + scaled_h:
                self.setCursor(Qt.CursorShape.CrossCursor)
                # преобразуем координаты в координаты изображения
                x_img = int((pos.x() - offset_x) * pixmap.width() / scaled_w)
                y_img = int((pos.y() - offset_y) * pixmap.height() / scaled_h)
                self.mouse_moved.emit(x_img, y_img)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)
        super().mouseMoveEvent(event)


    def leaveEvent(self, event):
        """Когда мышь выходит — возвращаем обычный курсор."""
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)