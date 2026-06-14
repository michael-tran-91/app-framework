from PySide6.QtCore import (
    Qt,
    Property,
    QPropertyAnimation,
    QEasingCurve,
    QTimer,
)
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (
    QScrollBar,
    QStyle,
    QStyleOptionSlider,
)


class AnimatedScrollBar(QScrollBar):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)

        self._opacity = 0.0
        self._handle_color = QColor("#808080")
        self._hover_color = QColor("#a0a0a0")
        self._handle_radius = 4
        self._hovered = False

        self.setMouseTracking(True)

        self._animation = QPropertyAnimation(self, b"opacity", self)
        self._animation.setDuration(150)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)

        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.setInterval(1200)
        self._hide_timer.timeout.connect(self.fade_out)

        self.valueChanged.connect(self.show_temporarily)
        self.setProperty("role", "default")

    # ==========================================================
    # opacity property
    # ==========================================================

    def getOpacity(self):
        return self._opacity

    def setOpacity(self, value):
        self._opacity = max(0.0, min(1.0, float(value)))
        self.update()

    opacity = Property(float, getOpacity, setOpacity)

    # ==========================================================
    # stylesheet properties
    # ==========================================================

    def getHandleColor(self):
        return self._handle_color

    def setHandleColor(self, color):
        self._handle_color = QColor(color)
        self.update()

    handleColor = Property(
        QColor,
        getHandleColor,
        setHandleColor,
    )

    def getHoverColor(self):
        return self._hover_color

    def setHoverColor(self, color):
        self._hover_color = QColor(color)
        self.update()

    hoverColor = Property(
        QColor,
        getHoverColor,
        setHoverColor,
    )

    def getHandleRadius(self):
        return self._handle_radius

    def setHandleRadius(self, value):
        self._handle_radius = int(value)
        print(f"set handle radius: {self._handle_radius}")
        self.update()

    handleRadius = Property(
        int,
        getHandleRadius,
        setHandleRadius,
    )

    # ==========================================================
    # animation helpers
    # ==========================================================

    def animate_to(self, value):
        self._animation.stop()
        self._animation.setStartValue(self._opacity)
        self._animation.setEndValue(value)
        self._animation.start()

    def fade_in(self):
        self.animate_to(1.0)

    def fade_out(self):
        if self._hovered:
            return

        self.animate_to(0.0)

    def show_temporarily(self):
        self.fade_in()
        self._hide_timer.start()

    # ==========================================================
    # events
    # ==========================================================

    def enterEvent(self, event):
        self._hovered = True
        self._hide_timer.stop()
        self.fade_in()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self._hide_timer.start()
        super().leaveEvent(event)

    # ==========================================================
    # painting
    # ==========================================================

    def paintEvent(self, event):
        if self.maximum() <= self.minimum():
            return

        if self._opacity <= 0.001:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        opt = QStyleOptionSlider()
        self.initStyleOption(opt)

        handle_rect = self.style().subControlRect(
            QStyle.CC_ScrollBar,
            opt,
            QStyle.SC_ScrollBarSlider,
            self,
        )

        color = (
            self._hover_color
            if self._hovered
            else self._handle_color
        )

        color = QColor(color)
        color.setAlphaF(self._opacity)

        painter.setPen(Qt.NoPen)
        painter.setBrush(color)

        if self.orientation() == Qt.Vertical:
            handle_rect.adjust(2, 2, -2, -2)
        else:
            handle_rect.adjust(2, 2, -2, -2)

        painter.drawRoundedRect(
            handle_rect,
            self._handle_radius,
            self._handle_radius,
        )