from .widget_controller import WidgetController
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtCore import Qt

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF, Property, QPropertyAnimation, Signal, QSize
from PySide6.QtGui import QPainter, QColor

class AnimatedToggle(QWidget):
    toggled = Signal(bool)

    def __init__(self, parent=None, thumb_margin=3, checked_position="right"):
        """
        checked_position: "right" or "left"
        """
        super().__init__(parent)
        self._checked = False
        self._offset = 0.0                 # animation parameter 0.0..1.0
        # Use a custom property name to avoid clashing with QWidget.pos()
        self._anim = QPropertyAnimation(self, b"offset", self)
        self._anim.setDuration(160)
        self._thumb_margin = thumb_margin
        # default colors (can be overridden by QSS using qproperty-onColor / qproperty-offColor)
        self._on_color = QColor("#4caf50")
        self._off_color = QColor("#d0d0d0")
        self.setCursor(Qt.PointingHandCursor)

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

        # track color (read from properties so QSS can override via qproperty-...)
        track_color = self._on_color if self._checked else self._off_color

        # draw track
        track_rect = QRectF(0, 0, w, h)
        painter.setBrush(track_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(track_rect, radius, radius)

        # compute thumb geometry
        thumb_d = h - 2 * self._thumb_margin
        x_min = self._thumb_margin
        x_max = w - self._thumb_margin - thumb_d

        if self.checked_position == "right":
            x = x_min + (x_max - x_min) * self._offset
        else:
            x = x_max - (x_max - x_min) * self._offset

        thumb_rect = QRectF(x, self._thumb_margin, thumb_d, thumb_d)
        painter.setBrush(QColor("white"))
        painter.drawEllipse(thumb_rect)

    # Animated property (use a unique name 'offset' to avoid QWidget.pos conflict)
    def getOffset(self):
        return self._offset

    def setOffset(self, v):
        self._offset = float(v)
        self.update()

    offset = Property(float, getOffset, setOffset)

    # Color properties exposed to QSS via `qproperty-<name>`
    def getOnColor(self):
        return self._on_color

    def setOnColor(self, c):
        # accept QColor or color string
        if isinstance(c, QColor):
            self._on_color = c
        else:
            self._on_color = QColor(str(c))
        self.update()

    onColor = Property(QColor, getOnColor, setOnColor)

    def getOffColor(self):
        return self._off_color

    def setOffColor(self, c):
        if isinstance(c, QColor):
            self._off_color = c
        else:
            self._off_color = QColor(str(c))
        self.update()

    offColor = Property(QColor, getOffColor, setOffColor)

    # State management
    def isChecked(self):
        return self._checked

    def setChecked(self, checked: bool, animate: bool = True):
        if self._checked == checked:
            return
        self._checked = checked

        start = self._offset
        end = 1.0 if checked else 0.0

        if animate:
            self._anim.stop()
            self._anim.setStartValue(start)
            self._anim.setEndValue(end)
            self._anim.start()
        else:
            self.setOffset(end)

        self.toggled.emit(checked)
        # Ensure layout systems recalc stable geometry after state change
        self.updateGeometry()

    def toggle(self):
        self.setChecked(not self._checked)

    # convenience
    def sizeHint(self):
        # Provide a stable preferred size so layouts don't collapse on interaction
        h = max(16, self.fontMetrics().height() + 8)
        w = int(h * 2.2)
        return QSize(w, h)

    def minimumSizeHint(self):
        h = 12
        w = int(h * 2)
        return QSize(w, h)

class ToggleController(WidgetController):

    def __init__(self):
        super().__init__(layout=None, widget=AnimatedToggle(checked_position="right"))
        self.widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.widget.setObjectName("Toggle")
        self.widget.setCursor(Qt.PointingHandCursor)
        self.widget.toggled.connect(self._toggled)

    def _toggled(self, checked):
        self.bubble_event({
            "type" : "toggle_controller_clicked",
            "data" : {
                "checked" : checked
            }
        })