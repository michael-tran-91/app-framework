import sys
from PySide6.QtWidgets import (QApplication, QSizePolicy, QVBoxLayout)
from PySide6.QtCore import QTimer
from core.controller.root_controller import RootController
from graphic.controller.widget_controller import WidgetController
from graphic.controller.shadow_edge_controller import ShadowEdgeController
from graphic.controller.stacked_controller import StackedController

styleSheet = """
QWidget#shadow_edge {
	background-color: #f3f6f7;
	border: none;
	qproperty-shadowAlpha: 50;
    qproperty-shadowSize: 6;
	qproperty-shadowColor: rgb(140, 140, 140);
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

	widget = root_ctrl.add_child(WidgetController(layout=QVBoxLayout()))
	shadow = widget.add_child(ShadowEdgeController())
	widget.widget.resize(400, 300)
	widget.widget.show()
	sys.exit(app.exec())


if __name__ == "__main__":
	main()
