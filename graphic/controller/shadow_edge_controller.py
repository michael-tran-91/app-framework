from .widget_controller import WidgetController
from core.controller.controller import Event
from PySide6.QtWidgets import QLayout, QSizePolicy, QStackedLayout, QFrame, QVBoxLayout, QHBoxLayout, QWidget
from enum import Enum
from PySide6.QtCore import Qt

class ShadowEdgeController(WidgetController):

    VERTICAL = 0
    HORIZONTAL = 1

    TOP     = 0b0001
    RIGHT   = 0b0010
    BOTTOM  = 0b0100
    LEFT    = 0b1000

    def __init__(self, direction:int = VERTICAL):
        self._stack_layout = QStackedLayout()
        self._stack_layout.setStackingMode(QStackedLayout.StackAll)
        super().__init__(layout=self._stack_layout, widget=QFrame())

        if direction == self.VERTICAL:
            self._content_layout = QVBoxLayout()
        else:
            self._content_layout = QHBoxLayout()
        self._content_widget = QWidget()
        self._content_widget.setLayout(self._content_layout)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(0)
        self._content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._stack_layout.addWidget(self._content_widget)
        self._stack_layout.setCurrentIndex(self._stack_layout.count() - 1)

        self._edges = {}

#---------------------------------------------------------------------------
# property
#---------------------------------------------------------------------------
    @property
    def layout(self):
        return self._content_layout
    
#---------------------------------------------------------------------------
# public method | enable edge shadows
#---------------------------------------------------------------------------
    def handle_set(self, event: Event):
        super().handle_set(event)
        if "side" in event.data:
            for dir in [self.TOP, self.RIGHT, self.BOTTOM, self.LEFT]:
                if event.data["side"] & dir:
                    if dir not in self._edges:
                        self._enable_edge(dir)
                    else:
                        self._edges[dir].show()

    def _enable_edge(self, direction):

        # if direction is top: create vertical layout, add qframe with fixed height and stretch remaining. add layout to stack
        edge = QFrame()
        edge.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self._edges[direction] = edge
        if direction == self.TOP:
            edge.setProperty("role", "shadow_edge_top")
            edge.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            layout_widget = QWidget()
            layout_widget.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            layout_widget.setLayout(layout)
            layout_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addWidget(edge)
            layout.addStretch()
            self._stack_layout.addWidget(layout_widget)
        elif direction == self.RIGHT:
            edge.setProperty("role", "shadow_edge_right")
            edge.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)            
            layout_widget = QWidget()
            layout_widget.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            layout_widget.setLayout(layout)
            layout_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addStretch()
            layout.addWidget(edge)
            self._stack_layout.addWidget(layout_widget)
        elif direction == self.BOTTOM:
            edge.setProperty("role", "shadow_edge_bottom")
            edge.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)            
            layout_widget = QWidget()
            layout_widget.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            layout_widget.setLayout(layout)
            layout_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addStretch()
            layout.addWidget(edge)
            self._stack_layout.addWidget(layout_widget)
        elif direction == self.LEFT:
            edge.setProperty("role", "shadow_edge_left")
            edge.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            layout_widget = QWidget()
            layout_widget.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            layout_widget.setLayout(layout)
            layout_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addWidget(edge)
            layout.addStretch()
            self._stack_layout.addWidget(layout_widget)

        self._stack_layout.setCurrentIndex(self._stack_layout.count() - 1)

