from .widget_controller import WidgetController, Event
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class ButtonController(WidgetController):

    def __init__(self):
        super().__init__(layout=None, widget=QPushButton("Click"))
        self.widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.widget.setProperty("role", "default")
        self.widget.setCursor(Qt.PointingHandCursor)

        button = self.widget
        button.clicked.connect(self._on_click)

    def _on_click(self):
        self.bubble_event(Event(event_type="button_controller_clicked", data={}))

    def handle_set(self, event: Event):
        super().handle_set(event)
        if "text" in event.data:
            self.widget.setText(event.data["text"])
        if "shadow" in event.data:
            if event.data["shadow"] == True:
                button = self.widget
                shadow = QGraphicsDropShadowEffect(button)
                shadow.setBlurRadius(4)
                shadow.setOffset(0, 0)  # shadow all around
                shadow.setColor(QColor(0, 0, 0, 120))

                button.setGraphicsEffect(shadow)