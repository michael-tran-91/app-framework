import sys
from PySide6.QtWidgets import (QApplication, QSizePolicy, QVBoxLayout)
from PySide6.QtCore import QTimer
from core.controller.root_controller import RootController
from graphic.controller.widget_controller import WidgetController
from graphic.controller.shadow_edge_controller import ShadowEdgeController
from graphic.controller.stacked_controller import StackedController
from graphic.controller.splitter_controller import SplitterController
from PySide6.QtCore import Qt

styleSheet = """
QWidget#shadow_edge {
	background-color: #f3f4f6;
	border: none;
	qproperty-shadowAlpha: 200;
    qproperty-shadowSize: 8;
	qproperty-shadowColor: rgb(0, 0, 0);
}
QWidget#test_widget {
	background-color: #e3e4e6;
	border: none;
}
QWidget#test_widget2 {
	background-color: #f3f4f6;
	border: none;
}

QFrame#shadow_edge_top {
    min-height: 10px;
	max-height: 10px;
	background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 5), stop:1 rgba(0, 0, 0, 0));
}

QFrame#shadow_edge_bottom {
	min-height: 10px;
	max-height: 10px;
	background: qlineargradient(x1:0, y1:1, x2:0, y2:0, stop:0 rgba(0, 0, 0, 5), stop:1 rgba(0, 0, 0, 0));
}

QFrame#shadow_edge_left{
	min-width: 10px;
	max-width: 10px;
	background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 5), stop:1 rgba(0, 0, 0, 0));
}

QFrame#shadow_edge_right {
	min-width: 10px;
	max-width: 10px;
	background: qlineargradient(x1:1, y1:0, x2:0, y2:0, stop:0 rgba(0, 0, 0, 5), stop:1 rgba(0, 0, 0, 0));
}
"""

def main():
	app = QApplication(sys.argv)
	app.setStyleSheet(styleSheet)

	root_ctrl = RootController()
	timer = QTimer()
	timer.setInterval(16)
	timer.timeout.connect(root_ctrl.process_events)
	timer.start()

	splitter = root_ctrl.add_child(SplitterController(orientation=Qt.Horizontal))

	widget = splitter.add_child(WidgetController(layout=QVBoxLayout()))
	shadow = widget.add_child(ShadowEdgeController(layout=QVBoxLayout()))
	shadow.enable_edge(ShadowEdgeController.TOP | ShadowEdgeController.RIGHT | ShadowEdgeController.BOTTOM | ShadowEdgeController.LEFT)
	a = shadow.add_child(WidgetController(layout=QVBoxLayout()))
	a.widget.setObjectName("test_widget")

	widget = splitter.add_child(WidgetController(layout=QVBoxLayout()))
	shadow = widget.add_child(ShadowEdgeController(layout=QVBoxLayout()))
	shadow.enable_edge(ShadowEdgeController.TOP | ShadowEdgeController.RIGHT | ShadowEdgeController.BOTTOM | ShadowEdgeController.LEFT)
	a = shadow.add_child(WidgetController(layout=QVBoxLayout()))
	a.widget.setObjectName("test_widget2")
	splitter.widget.resize(400, 300)
	splitter.widget.show()
	sys.exit(app.exec())


if __name__ == "__main__":
	main()
