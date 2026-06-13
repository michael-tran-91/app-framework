from .widget_controller import WidgetController
from PySide6.QtWidgets import QLabel, QSizePolicy

class LabelController(WidgetController):

    def __init__(self, text: str | None = None):
        super().__init__(layout=None, widget=QLabel())
        self.widget.setWordWrap(True)
        self.widget.setText(text)