from ..controller.vertical_controller import VerticalController
from ..controller.horizontal_controller import HorizontalController
from ..controller.shadow_edge_controller import ShadowEdgeController
from ..controller.button_controller import ButtonController
from ..controller.widget_controller import Event
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

class WindowController(VerticalController):

    def __init__(self):
        super().__init__()
        self.widget.setWindowFlags(
            Qt.Window | Qt.FramelessWindowHint
        )

    def _on_attached(self):
        super()._on_attached()

        self._title_bar = self.add_child(HorizontalController())
        self._title_bar.dispatch_event(Event(event_type="set", data={
            "role" : "title_bar",
            "size_policy" : ["expanding", "fixed"],
            "height" : 40,
            "notify_mouse_events" : True
        }))
        self._title_bar.add_child(HorizontalController())
        self._control_button = self._title_bar.add_child(HorizontalController())
        self._control_button.dispatch_event(Event(event_type="set", data={
            "size_policy" : ["maximum", "expanding"]
        }))
        self._minimize_button = self._control_button.add_child(ButtonController())
        self._minimize_button.dispatch_event(Event(event_type="set", data={
            "role" : "minimize_button",
            "text" : "—",
            "size_policy" : ["fixed", "expanding"],
            "width" : 50
        }))
        self._maximize_button = self._control_button.add_child(ButtonController())
        self._maximize_button.dispatch_event(Event(event_type="set", data={
            "role" : "minimize_button",
            "text" : "—",
            "size_policy" : ["fixed", "expanding"],
            "width" : 50
        }))
        self._exit_button = self._control_button.add_child(ButtonController())
        self._exit_button.dispatch_event(Event(event_type="set", data={
            "role" : "exit_button",
            "text" : "✕",
            "size_policy" : ["fixed", "expanding"],
            "width" : 50
        }))

        self._main_content = self.add_child(ShadowEdgeController(direction=ShadowEdgeController.VERTICAL))
        self._main_content.dispatch_event(Event(event_type="set", data={
            "side" : ShadowEdgeController.TOP
        }))

        self.register_event_handler("button_controller_clicked", self.handle_exit_button_clicked, required_controllers=[
            self._exit_button
        ])

        self.register_event_handler("mouse_event", self.handle_title_bar_movement, required_controllers=[
            self._title_bar
        ])

    def handle_title_bar_movement(self, event: Event):
        self.widget.window().windowHandle().startSystemMove()

    def handle_exit_button_clicked(self, event: Event):
        QApplication.instance().quit()