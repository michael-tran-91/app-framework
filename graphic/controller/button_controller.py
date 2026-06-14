from .widget_controller import WidgetController
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class ButtonController(WidgetController):

    def __init__(self):
        super().__init__(layout=None, widget=QPushButton("Click"))
        self.widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.widget.setProperty("role", "default")
        self.widget.setCursor(Qt.PointingHandCursor)

        button = self.widget
        shadow = QGraphicsDropShadowEffect(button)
        shadow.setBlurRadius(4)
        shadow.setOffset(0, 0)  # shadow all around
        shadow.setColor(QColor(0, 0, 0, 120))

        button.setGraphicsEffect(shadow)