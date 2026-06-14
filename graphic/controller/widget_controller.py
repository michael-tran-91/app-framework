from core.controller.controller import Controller, Event
from PySide6.QtWidgets import QLayout, QSizePolicy, QWidget, QLabel
from PySide6.QtCore import Qt, QObject, QEvent

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
        self._mouse_event_filter = None

    def _on_attached(self):
        super()._on_attached()
        self.register_event_handler("set", self.handle_set)

    class MouseEventFilter(QObject):
        def __init__(self, controller):
            super().__init__(None)
            self._controller = controller

        def _resize_edges(self, pos):
            x = pos.x()
            y = pos.y()

            w = self._controller.widget.width()
            h = self._controller.widget.height()

            m = 8

            left = x <= m
            right = x >= w - m

            top = y <= m
            bottom = y >= h - m

            if top and left:
                return Qt.TopEdge | Qt.LeftEdge

            if top and right:
                return Qt.TopEdge | Qt.RightEdge

            if bottom and left:
                return Qt.BottomEdge | Qt.LeftEdge

            if bottom and right:
                return Qt.BottomEdge | Qt.RightEdge

            if left:
                return Qt.LeftEdge

            if right:
                return Qt.RightEdge

            if top:
                return Qt.TopEdge

            if bottom:
                return Qt.BottomEdge

            return None

        def eventFilter(self, obj, event):
            if event.type() == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    self._controller.bubble_event(Event(event_type="mouse_event", data={
                        "type" : "press",
                        "global_position": event.globalPosition().toPoint()
                    }))
                    return True
            elif event.type() == QEvent.MouseButtonRelease:
                if event.button() == Qt.LeftButton:
                    self._controller.bubble_event(Event(event_type="mouse_event", data={
                        "type" : "release",
                        "global_position": event.globalPosition().toPoint()
                    }))
                    return True
            elif event.type() == QEvent.MouseMove:
                if event.buttons() & Qt.LeftButton:
                    self._controller.bubble_event(Event(event_type="mouse_event", data={
                        "type" : "move",
                        "global_position": event.globalPosition().toPoint()
                    }))
                else:
                    self._controller.bubble_event(Event(event_type="mouse_event", data={
                        "type" : "hover",
                        "global_position": event.globalPosition().toPoint(),
                        "resize_edges" : self._resize_edges(event.position().toPoint())
                    }))
                    return True

            return False

    def handle_set(self, event: Event):
        if "notify_mouse_events" in event.data:
            enable = event.data["notify_mouse_events"]
            if enable:
                if self._mouse_event_filter is None:
                    self._mouse_event_filter = WidgetController.MouseEventFilter(self)
                    self.widget.installEventFilter(self._mouse_event_filter)
                    self.widget.setMouseTracking(True)
            else:
                if self._mouse_event_filter is not None:
                    self.widget.removeEventFilter(self._mouse_event_filter)
                    self._mouse_event_filter = None
                    self.widget.setMouseTracking(False)
        if "role" in event.data:
            self.widget.setProperty("role", event.data["role"])
        if "width" in event.data:
            self.widget.setMinimumWidth(event.data["width"])
            self.widget.setMaximumWidth(event.data["width"])
        if "height" in event.data:
            self.widget.setMinimumHeight(event.data["height"])
            self.widget.setMaximumHeight(event.data["height"])
        if "fixed_width" in event.data:
            self.widget.setFixedWidth(event.data["fixed_width"])
        if "fixed_height" in event.data:
            self.widget.setFixedHeight(event.data["fixed_height"])
        if "content_margins" in event.data:
            target = self.layout if self.layout is not None else self.widget
            target.setContentsMargins(
                event.data["content_margins"][0],
                event.data["content_margins"][1],
                event.data["content_margins"][2],
                event.data["content_margins"][3])
        if "spacing" in event.data:
            if self.layout:
                self.layout.setSpacing(event.data["spacing"])
        if "size_policy" in event.data:
            width_policy = QSizePolicy.Policy.Expanding
            height_policy = QSizePolicy.Policy.Expanding
            data_policy = event.data["size_policy"]
            if data_policy[0] == "fixed":
                width_policy = QSizePolicy.Policy.Fixed
            elif data_policy[0] == "maximum":
                width_policy = QSizePolicy.Policy.Maximum
            elif data_policy[0] == "minimum":
                width_policy = QSizePolicy.Policy.Minimum

            if data_policy[1] == "fixed":
                height_policy = QSizePolicy.Policy.Fixed
            elif data_policy[1] == "maximum":
                height_policy = QSizePolicy.Policy.Maximum
            elif data_policy[1] == "minimum":
                height_policy = QSizePolicy.Policy.Minimum

            self.widget.setSizePolicy(width_policy, height_policy)

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