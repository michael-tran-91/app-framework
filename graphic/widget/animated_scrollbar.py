from PySide6.QtCore import (
    Qt,
    QObject,
    QEvent,
    QTimer,
    Property,
    QEasingCurve,
    QPropertyAnimation,
)
from PySide6.QtGui import (
    QColor,
    QPainter,
)
from PySide6.QtWidgets import (
    QScrollBar,
    QStyle,
    QStyleOptionSlider,
)

class AnimatedScrollBar(QScrollBar):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)

        self._opacity = 0.0
        self._handleColor = QColor("#c7c7c7")
        self._hoverColor = QColor("#c7c7c7")
        self._radius = 4
        self._mouseOnViewport = False
        self._mouseOnScrollbar = False

        self.setMouseTracking(True)
        # animation
        self._animation = QPropertyAnimation(
            self,
            b"opacity",
            self,
        )
        self._animation.setDuration(400)
        self._animation.setEasingCurve(
            QEasingCurve.OutCubic
        )
        # hide timer
        self._hideTimer = QTimer(self)
        self._hideTimer.setSingleShot(True)
        self._hideTimer.setInterval(800)
        self._hideTimer.timeout.connect(
            self.fadeOut
        )
        self.valueChanged.connect(
            self.showTemporarily
        )

        self.setProperty("role", "default")

    # =====================================================
    # Install on scroll area
    # =====================================================

    def attachTo(self, scrollArea):
        viewport = scrollArea.viewport()

        viewport.setMouseTracking(True)
        viewport.installEventFilter(self)

    # =====================================================
    # Properties
    # =====================================================

    def getOpacity(self):
        return self._opacity

    def setOpacity(self, value):
        self._opacity = max(
            0.0,
            min(
                1.0,
                float(value),
            ),
        )

        self.update()

    opacity = Property(
        float,
        getOpacity,
        setOpacity,
    )

    # -------------------------

    def getHandleColor(self):
        return self._handleColor

    def setHandleColor(self, value):
        self._handleColor = QColor(value)
        self.update()

    handleColor = Property(
        QColor,
        getHandleColor,
        setHandleColor,
    )

    # -------------------------

    def getHoverColor(self):
        return self._hoverColor

    def setHoverColor(self, value):
        self._hoverColor = QColor(value)
        self.update()

    hoverColor = Property(
        QColor,
        getHoverColor,
        setHoverColor,
    )

    # -------------------------

    def getRadius(self):
        return self._radius

    def setRadius(self, value):
        self._radius = int(value)
        self.update()

    radius = Property(
        int,
        getRadius,
        setRadius,
    )

    # =====================================================
    # Animation
    # =====================================================

    def animateTo(self, target):
        self._animation.stop()

        self._animation.setStartValue(
            self._opacity
        )

        self._animation.setEndValue(
            target
        )

        self._animation.start()

    def fadeIn(self):
        self.animateTo(1.0)

    def fadeOut(self):
        if (
            self._mouseOnViewport
            or self._mouseOnScrollbar
        ):
            return

        self.animateTo(0.0)

    # =====================================================
    # Activity
    # =====================================================

    def showTemporarily(self):
        self.fadeIn()

        if (
            not self._mouseOnViewport
            and not self._mouseOnScrollbar
        ):
            self._hideTimer.start()

    # =====================================================
    # Mouse events
    # =====================================================

    def enterEvent(self, event):
        self._mouseOnScrollbar = True

        self._hideTimer.stop()

        self.fadeIn()

        super().enterEvent(event)

    def leaveEvent(self, event):
        self._mouseOnScrollbar = False

        if not self._mouseOnViewport:
            self._hideTimer.start()

        super().leaveEvent(event)

    # =====================================================
    # Viewport tracking
    # =====================================================

    def eventFilter(
        self,
        obj,
        event,
    ):
        if event.type() == QEvent.Enter:

            self._mouseOnViewport = True

            self._hideTimer.stop()

            self.fadeIn()

        elif event.type() == QEvent.Leave:

            self._mouseOnViewport = False

            if not self._mouseOnScrollbar:
                self._hideTimer.start()

        return False

    # =====================================================
    # Paint
    # =====================================================

    def paintEvent(self, event):

        if self.maximum() <= self.minimum():
            return

        if self._opacity <= 0.001:
            return

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        opt = QStyleOptionSlider()

        self.initStyleOption(opt)

        handleRect = (
            self.style().subControlRect(
                QStyle.CC_ScrollBar,
                opt,
                QStyle.SC_ScrollBarSlider,
                self,
            )
        )

        color = (
            self._hoverColor
            if (
                self._mouseOnViewport
                or self._mouseOnScrollbar
            )
            else self._handleColor
        )

        color = QColor(color)

        color.setAlphaF(
            self._opacity
        )

        painter.setPen(
            Qt.NoPen
        )

        painter.setBrush(
            color
        )

        handleRect.adjust(
            1,
            1,
            -1,
            -1,
        )

        painter.drawRoundedRect(
            handleRect,
            self._radius,
            self._radius,
        )