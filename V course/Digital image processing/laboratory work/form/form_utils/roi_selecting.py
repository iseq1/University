"""
Вспомогательная форма для выбора ROI на изображении
"""
from PyQt6.QtCore import pyqtSignal, QRect, Qt
from PyQt6.QtGui import QPainter, QPen

from form.form_utils.mouse_tracking import MouseTracker


class ROISelector(MouseTracker):
    """Форма для выбора ROI на изображении"""

    roi_selected = pyqtSignal(QRect)  # сигнал, когда выделили область

    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_pos = None
        self.end_pos = None
        self.drawing = False

    def mousePressEvent(self, event):
        """Обработчик нажатия мыши"""

        if event.button() == Qt.MouseButton.LeftButton:
            if self._inside_pixmap(event.pos()):

                self.start_pos = event.pos()
                self.end_pos = self.start_pos
                self.drawing = True
                self.update()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Обработчик движения мыши"""

        if self.drawing and self._inside_pixmap(event.pos()):
            self.end_pos = event.pos()
            self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Обработчик события отжатия ЛКМ"""
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            rect = QRect(self.start_pos, self.end_pos).normalized()
            rect = self._clip_to_pixmap(rect)
            self.roi_selected.emit(rect)
            self.update()
        super().mouseReleaseEvent(event)

    def _inside_pixmap(self, pos):
        """Проверка, что позиция внутри картинки"""
        pixmap = self.pixmap()
        if not pixmap:
            return False
        scaled_w = pixmap.width()
        scaled_h = pixmap.height()
        offset_x = (self.width() - scaled_w) // 2
        offset_y = (self.height() - scaled_h) // 2
        return offset_x <= pos.x() <= offset_x + scaled_w and offset_y <= pos.y() <= offset_y + scaled_h

    def _clip_to_pixmap(self, rect):
        """Обрезаем ROI по границам картинки"""
        pixmap = self.pixmap()
        if not pixmap:
            return rect
        scaled_w = pixmap.width()
        scaled_h = pixmap.height()
        offset_x = (self.width() - scaled_w) // 2
        offset_y = (self.height() - scaled_h) // 2
        x1 = max(rect.left(), offset_x)
        y1 = max(rect.top(), offset_y)
        x2 = min(rect.right(), offset_x + scaled_w)
        y2 = min(rect.bottom(), offset_y + scaled_h)
        return QRect(x1, y1, x2 - x1, y2 - y1)

    def paintEvent(self, event):
        """Обработчик отображения границ ROI"""

        super().paintEvent(event)
        if self.start_pos and self.end_pos and self.drawing:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.GlobalColor.red, 2, Qt.PenStyle.DashLine))
            rect = QRect(self.start_pos, self.end_pos)
            painter.drawRect(rect)