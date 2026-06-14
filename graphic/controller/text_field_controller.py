from .widget_controller import WidgetController
from core.controller.controller import Event
from PySide6.QtWidgets import QLineEdit, QWidget, QSizePolicy

class TextFieldController(WidgetController):

    def __init__(self):
        super().__init__(layout = None, widget = QLineEdit())
        self.widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.widget.setProperty("role", "default")

    def _on_attached(self):
        super()._on_attached()
        self.register_event_handler("set", self.handle_set)

    def handle_set(self, event: Event):
        if "placeholder" in event.data:
            self.widget.setPlaceholderText(event.data["placeholder"])