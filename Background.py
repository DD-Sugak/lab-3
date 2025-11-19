from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt, QRect
import os

class BackgroundWidget(QWidget):
    """Базовый виджет с фоновым изображением"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_pixmap = None

    def set_background(self, image_path):
        if os.path.exists(image_path):
            self.background_pixmap = QPixmap(image_path)
            self.update()

    def paintEvent(self, event):
        """Заполняет весь виджет изображением (как background-size: cover)"""
        if self.background_pixmap and not self.background_pixmap.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

            widget_rect = self.rect()
            pixmap_size = self.background_pixmap.size()

            # Масштабируем чтобы изображение заполнило весь виджет (может обрезаться)
            scaled_pixmap = self.background_pixmap.scaled(
                widget_rect.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )

            # Центрируем обрезанное изображение
            x = (scaled_pixmap.width() - widget_rect.width()) // 2
            y = (scaled_pixmap.height() - widget_rect.height()) // 2

            painter.drawPixmap(widget_rect, scaled_pixmap, QRect(x, y, widget_rect.width(), widget_rect.height()))

        super().paintEvent(event)