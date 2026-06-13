from .widget_controller import WidgetController
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy, QPushButton
from PySide6.QtCore import Qt

class ButtonController(WidgetController):

    def __init__(self):
        super().__init__(layout=None, widget=QPushButton("Click"))
        self.widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.widget.setObjectName("Button")
        self.widget.setCursor(Qt.PointingHandCursor)