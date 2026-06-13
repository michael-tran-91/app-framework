from .widget_controller import WidgetController
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy, QPushButton, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor

class ButtonController(WidgetController):

    def __init__(self):
        super().__init__(layout=None, widget=QPushButton("Click"))
        self.widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)