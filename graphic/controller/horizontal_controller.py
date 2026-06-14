from .widget_controller import WidgetController
from PySide6.QtWidgets import QHBoxLayout

class HorizontalController(WidgetController):

    def __init__(self):
        super().__init__(layout=QHBoxLayout())