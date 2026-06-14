from .widget_controller import WidgetController
from PySide6.QtWidgets import QLineEdit, QWidget, QSizePolicy

class TextFieldController(WidgetController):

    def __init__(self):
        super().__init__(layout = None, widget = QLineEdit())
        self.widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.widget.setProperty("role", "default")

    def set_placeholder(self, text: str):
        self.widget.setPlaceholderText(text)

    def set_label(self, text: str):
        pass