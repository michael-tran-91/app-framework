from .widget_controller import WidgetController
from PySide6.QtWidgets import QLayout, QWidget
from PySide6.QtGui import QPainter, QColor, QLinearGradient
from PySide6.QtCore import Property, QRect

class ShadowEdgeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("shadow_edge")
        self._shadow_alpha = 50
        self._shadow_size = 5
        self._shadow_color = QColor(140, 140, 140)

    def getShadowAlpha(self):
        return self._shadow_alpha

    def setShadowAlpha(self, value):
        self._shadow_alpha = value
        self.update()

    def getShadowSize(self):
        return self._shadow_size

    def setShadowSize(self, value):
        self._shadow_size = value
        self.update()

    def getShadowColor(self):
        return self._shadow_color
    
    def setShadowColor(self, value):
        self._shadow_color = value
        self.update()

    shadowAlpha = Property(int, getShadowAlpha, setShadowAlpha)
    shadowSize = Property(int, getShadowSize, setShadowSize)
    shadowColor = Property(QColor, getShadowColor, setShadowColor)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()

        # Fill background
        bg_color = self.palette().color(self.backgroundRole())
        painter.fillRect(rect, bg_color)

        shadow_alpha = self._shadow_alpha
        shadow_size = self._shadow_size

        # Top edge gradient
        grad_top = QLinearGradient(0, 0, 0, shadow_size)
        grad_top.setColorAt(0, QColor(self._shadow_color.red(), self._shadow_color.green(), self._shadow_color.blue(), shadow_alpha))
        grad_top.setColorAt(1, QColor(self._shadow_color.red(), self._shadow_color.green(), self._shadow_color.blue(), 0))
        painter.fillRect(QRect(0, 0, rect.width(), shadow_size), grad_top)

        # Bottom edge gradient
        grad_bottom = QLinearGradient(0, rect.height()-shadow_size, 0, rect.height())
        grad_bottom.setColorAt(0, QColor(self._shadow_color.red(), self._shadow_color.green(), self._shadow_color.blue(), 0))
        grad_bottom.setColorAt(1, QColor(self._shadow_color.red(), self._shadow_color.green(), self._shadow_color.blue(), shadow_alpha))
        painter.fillRect(QRect(0, rect.height()-shadow_size, rect.width(), shadow_size), grad_bottom)

        # Left edge gradient
        grad_left = QLinearGradient(0, 0, shadow_size, 0)
        grad_left.setColorAt(0, QColor(self._shadow_color.red(), self._shadow_color.green(), self._shadow_color.blue(), shadow_alpha))
        grad_left.setColorAt(1, QColor(self._shadow_color.red(), self._shadow_color.green(), self._shadow_color.blue(), 0))
        painter.fillRect(QRect(0, 0, shadow_size, rect.height()), grad_left)

        # Right edge gradient
        grad_right = QLinearGradient(rect.width()-shadow_size, 0, rect.width(), 0)
        grad_right.setColorAt(0, QColor(self._shadow_color.red(), self._shadow_color.green(), self._shadow_color.blue(), 0))
        grad_right.setColorAt(1, QColor(self._shadow_color.red(), self._shadow_color.green(), self._shadow_color.blue(), shadow_alpha))
        painter.fillRect(QRect(rect.width()-shadow_size, 0, shadow_size, rect.height()), grad_right)

class ShadowEdgeController(WidgetController):
    def __init__(self, layout: QLayout | None = None):
        super().__init__(layout=layout, widget=ShadowEdgeWidget())