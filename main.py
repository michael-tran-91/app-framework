import sys
from PySide6.QtWidgets import (QApplication, QSizePolicy, QVBoxLayout)
from PySide6.QtCore import QTimer
from core.controller.root_controller import RootController
from graphic.controller.widget_controller import WidgetController
from graphic.controller.shadow_edge_controller import ShadowEdgeController
from graphic.controller.stacked_controller import StackedController
from graphic.controller.splitter_controller import SplitterController
from graphic.controller.button_controller import ButtonController
from graphic.controller.toggle_controller import ToggleController
from PySide6.QtCore import Qt
from util.file_manager import fetch as fetch_file_content

light_styleSheet = fetch_file_content(path="app://res/theme/light.qss", encoding="utf8")
dark_styleSheet = fetch_file_content(path="app://res/theme/dark.qss", encoding="utf8")

def main():
	app = QApplication(sys.argv)
	app.setStyleSheet(light_styleSheet)

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
	btn = a.add_child(ButtonController())
	btn.widget.setFixedSize(200, 40)
	btn = a.add_child(ToggleController())
	btn.widget.setFixedSize(200, 40)

	splitter.widget.resize(400, 300)
	splitter.widget.show()
	sys.exit(app.exec())


if __name__ == "__main__":
	main()
