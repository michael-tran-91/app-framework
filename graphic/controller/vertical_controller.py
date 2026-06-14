from .widget_controller import WidgetController
from PySide6.QtWidgets import QVBoxLayout

class VerticalController(WidgetController):

    def __init__(self):
        super().__init__(layout=QVBoxLayout())