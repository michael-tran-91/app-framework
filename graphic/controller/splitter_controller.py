from .widget_controller import WidgetController
from core.controller.controller import Controller
from PySide6.QtWidgets import QSplitter

class SplitterController(WidgetController):
    def __init__(self, orientation):
        super().__init__(layout=None, widget=QSplitter(orientation))
        self.widget.setHandleWidth(0)

#---------------------------------------------------------------------------
# public method | tree structure
#---------------------------------------------------------------------------
    def add_child(self, child : Controller):
        super().add_child(child)
        self.widget.addWidget(child.widget)
        return child

    def remove_child(self, child : Controller):
        super().remove_child(child)
        self.widget.removeWidget(child.widget)