from .widget_controller import WidgetController
from core.controller.controller import Event
from PySide6.QtWidgets import QLabel, QSizePolicy

class LabelController(WidgetController):

    def __init__(self, text: str | None = None):
        super().__init__(layout=None, widget=QLabel())
        self.widget.setWordWrap(True)
        self.widget.setText(text)
        self._widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    def _on_attached(self):
        super()._on_attached()
        self.register_event_handler("set", self.handle_set)

    def handle_set(self, event: Event):
        if "text" in event.data:
            self.widget.setText(event.data["text"])