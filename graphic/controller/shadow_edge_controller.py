from .widget_controller import WidgetController
from PySide6.QtWidgets import QLayout, QSizePolicy, QStackedLayout, QFrame, QVBoxLayout, QHBoxLayout, QWidget
from enum import Enum

class ShadowEdgeController(WidgetController):

    TOP     = 0b0001
    RIGHT   = 0b0010
    BOTTOM  = 0b0100
    LEFT    = 0b1000

    def __init__(self, layout: QLayout | None = None):
        self._stack_layout = QStackedLayout()
        self._stack_layout.setStackingMode(QStackedLayout.StackAll)
        super().__init__(layout=self._stack_layout, widget=QFrame())

        self._content_layout = layout
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
    def enable_edge(self, direction):
        for dir in [self.TOP, self.RIGHT, self.BOTTOM, self.LEFT]:
            if direction & dir:
                if dir not in self._edges:
                    self._enable_edge(dir)
                else:
                    self._edges[dir].show()

    def _enable_edge(self, direction):

        # if direction is top: create vertical layout, add qframe with fixed height and stretch remaining. add layout to stack
        edge = QFrame()
        self._edges[direction] = edge
        if direction == self.TOP:
            edge.setObjectName("shadow_edge_top")
            edge.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            layout_widget = QWidget()
            layout_widget.setLayout(layout)
            layout_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addWidget(edge)
            layout.addStretch()
            self._stack_layout.addWidget(layout_widget)
        elif direction == self.RIGHT:
            edge.setObjectName("shadow_edge_right")
            edge.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)            
            layout_widget = QWidget()
            layout_widget.setLayout(layout)
            layout_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addStretch()
            layout.addWidget(edge)
            self._stack_layout.addWidget(layout_widget)
        elif direction == self.BOTTOM:
            edge.setObjectName("shadow_edge_bottom")
            edge.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)            
            layout_widget = QWidget()
            layout_widget.setLayout(layout)
            layout_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addStretch()
            layout.addWidget(edge)
            self._stack_layout.addWidget(layout_widget)
        elif direction == self.LEFT:
            edge.setObjectName("shadow_edge_left")
            edge.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            layout_widget = QWidget()
            layout_widget.setLayout(layout)
            layout_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addWidget(edge)
            layout.addStretch()
            self._stack_layout.addWidget(layout_widget)

        self._stack_layout.setCurrentIndex(self._stack_layout.count() - 1)

