from core.controller.controller import Controller, Event
from PySide6.QtWidgets import QLayout, QSizePolicy, QWidget, QLabel

class WidgetController(Controller):
    def __init__(self, layout: QLayout | None = None, widget: QWidget | None = None):
        super().__init__()
        self._layout = layout
        self._widget = widget if widget is not None else QWidget()
        if layout:
            self._widget.setLayout(layout)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
        self._widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def _on_attached(self):
        super()._on_attached()
        self.register_event_handler("set", self.handle_set)

    def handle_set(self, event: Event):
        if "role" in event.data:
            self.widget.setProperty("role", event.data["role"])

#---------------------------------------------------------------------------
# property
#---------------------------------------------------------------------------
    @property
    def layout(self):
        return self._layout
    
    @property
    def widget(self):
        return self._widget

#---------------------------------------------------------------------------
# public method | tree structure
#---------------------------------------------------------------------------
    def add_child(self, child : Controller):
        super().add_child(child)
        if isinstance(child, WidgetController) and self.layout:
            self.layout.addWidget(child.widget)
        return child

    def remove_child(self, child : Controller):
        if isinstance(child, WidgetController) and self.layout:
            self.layout.removeWidget(child.widget)

        super().remove_child(child)

#---------------------------------------------------------------------------
# private method
#---------------------------------------------------------------------------
    def _on_shutdown(self):
        if self._widget:
            self._widget.deleteLater()
        if self._layout:
            self._layout.deleteLater()

        super()._on_shutdown()