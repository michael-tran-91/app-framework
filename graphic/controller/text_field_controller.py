from .widget_controller import WidgetController
from core.controller.controller import Event
from PySide6.QtWidgets import QLineEdit, QWidget, QSizePolicy

class TextFieldController(WidgetController):

    def __init__(self):
        super().__init__(layout = None, widget = QLineEdit())
        self.widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.widget.setProperty("role", "default")

    def handle_set(self, event: Event):
        super().handle_set(event)
        if "placeholder" in event.data:
            self.widget.setPlaceholderText(event.data["placeholder"])