from .widget_controller import WidgetController
from core.controller.controller import Controller
from PySide6.QtWidgets import QStackedLayout

class StackedController(WidgetController):
    def __init__(self):
        super().__init__(layout = QStackedLayout())
        # set layout to display all widgets
        self.layout.setStackingMode(QStackedLayout.StackAll)

#---------------------------------------------------------------------------
# public method | tree structure
#---------------------------------------------------------------------------
    def add_child(self, child : Controller):
        super().add_child(child)
        if self.layout:
            self.layout.setCurrentIndex(len(self.childrens) - 1)
        return child

    def remove_child(self, child : Controller):
        super().remove_child(child)
        if self.layout:
            self.layout.setCurrentIndex(len(self.childrens) - 1)