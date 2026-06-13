from .widget_controller import WidgetController
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy, QPushButton
from PySide6.QtCore import Qt

from PySide6.QtWidgets import QWidget, QApplication, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QRectF, Property, QPropertyAnimation, Signal
from PySide6.QtGui import QPainter, QColor, QFont
import sys

class AnimatedToggle(QWidget):
    toggled = Signal(bool)

    def __init__(self, parent=None, thumb_margin=3, checked_position="right"):
        """
        checked_position: "right" or "left"
        """
        super().__init__(parent)
        self._checked = False
        self._pos = 0.0                 # animation parameter 0.0..1.0
        self._anim = QPropertyAnimation(self, b"pos", self)
        self._anim.setDuration(160)
        self._thumb_margin = thumb_margin
        self.setCursor(Qt.PointingHandCursor)

        # checked_position controls which side corresponds to checked state
        if checked_position not in ("right", "left"):
            raise ValueError("checked_position must be 'right' or 'left'")
        self.checked_position = checked_position

    # Mouse and keyboard interaction
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle()
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter):
            self.toggle()
        else:
            super().keyPressEvent(event)

    # Painting
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        radius = h / 2.0

        # track color
        on_color = QColor("#4caf50")
        off_color = QColor("#d0d0d0")
        track_color = on_color if self._checked else off_color

        # draw track
        track_rect = QRectF(0, 0, w, h)
        painter.setBrush(track_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(track_rect, radius, radius)

        # compute thumb geometry
        thumb_d = h - 2 * self._thumb_margin
        x_min = self._thumb_margin
        x_max = w - self._thumb_margin - thumb_d

        # If checked_position == "right": pos 0 -> left, pos 1 -> right
        # If checked_position == "left": pos 0 -> right, pos 1 -> left (inverted)
        if self.checked_position == "right":
            x = x_min + (x_max - x_min) * self._pos
        else:
            x = x_max - (x_max - x_min) * self._pos

        thumb_rect = QRectF(x, self._thumb_margin, thumb_d, thumb_d)
        painter.setBrush(QColor("white"))
        painter.drawEllipse(thumb_rect)

    # Animated property
    def getPos(self):
        return self._pos

    def setPos(self, v):
        self._pos = float(v)
        self.update()

    pos = Property(float, getPos, setPos)

    # State management
    def isChecked(self):
        return self._checked

    def setChecked(self, checked: bool, animate: bool = True):
        if self._checked == checked:
            return
        self._checked = checked

        start = self._pos
        end = 1.0 if checked else 0.0

        if animate:
            self._anim.stop()
            self._anim.setStartValue(start)
            self._anim.setEndValue(end)
            self._anim.start()
        else:
            self.setPos(end)

        self.toggled.emit(checked)

    def toggle(self):
        self.setChecked(not self._checked)

    # convenience
    def sizeHint(self):
        return self.size()

class ToggleController(WidgetController):

    def __init__(self):
        super().__init__(layout=None, widget=AnimatedToggle(checked_position="right"))
        self.widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.widget.setObjectName("Toggle")
        self.widget.setCursor(Qt.PointingHandCursor)