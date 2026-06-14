import sys
from PySide6.QtWidgets import (QApplication, QSizePolicy, QVBoxLayout, QHBoxLayout)
from PySide6.QtCore import QTimer
from core.controller.root_controller import RootController
from graphic.controller.widget_controller import WidgetController
from graphic.controller.shadow_edge_controller import ShadowEdgeController
from graphic.controller.stacked_controller import StackedController
from graphic.controller.splitter_controller import SplitterController
from graphic.controller.button_controller import ButtonController
from graphic.controller.toggle_controller import ToggleController
from graphic.controller.label_controller import LabelController
from graphic.controller.text_field_controller import TextFieldController
from PySide6.QtCore import Qt
from util.file_manager import fetch as fetch_file_content

light_styleSheet = fetch_file_content(path="app://res/theme/light.qss", encoding="utf8")
dark_styleSheet = fetch_file_content(path="app://res/theme/dark.qss", encoding="utf8")


def main():
	app = QApplication(sys.argv)
	app.setStyleSheet(light_styleSheet)

	light_dark_toggle = None
	lb = None

	def test_handle(event):
		if light_dark_toggle.in_event_context(event):
			if event["data"]["checked"]:
				app.setStyleSheet(light_styleSheet)
			else:
				app.setStyleSheet(dark_styleSheet)
			lb.widget.setText(lb.widget.text() + " append")
			return True
		
		return False

	root_ctrl = RootController()
	root_ctrl.register_event_handler("toggle_controller_clicked", test_handle)

	stack = root_ctrl.add_child(StackedController())
	stack.widget.setObjectName("main_background")
	splitter = stack.add_child(SplitterController(orientation=Qt.Horizontal))

	widget = splitter.add_child(WidgetController(layout=QVBoxLayout()))
	shadow = widget.add_child(ShadowEdgeController(layout=QVBoxLayout()))
	shadow.enable_edge(ShadowEdgeController.TOP | ShadowEdgeController.BOTTOM | ShadowEdgeController.LEFT)
	a = shadow.add_child(WidgetController(layout=QVBoxLayout()))
	a.widget.setProperty("role","test_widget")

	widget = splitter.add_child(WidgetController(layout=QVBoxLayout()))
	shadow = widget.add_child(ShadowEdgeController(layout=QVBoxLayout()))
	shadow.enable_edge(ShadowEdgeController.TOP | ShadowEdgeController.RIGHT | ShadowEdgeController.BOTTOM | ShadowEdgeController.LEFT)
	a = shadow.add_child(WidgetController(layout=QVBoxLayout()))
	a.widget.setProperty("role","test_widget2")
	btn = a.add_child(ButtonController())
	btn.widget.setFixedSize(200, 40)
	btn = a.add_child(ToggleController(True))
	btn.widget.setProperty("role","toggle_theme")
	btn.widget.setFixedSize(60, 30)
	light_dark_toggle = btn
	a = shadow.add_child(WidgetController(layout=QHBoxLayout()))
	lb = a.add_child(LabelController("Test Label"))
	a.add_child(LabelController("Test Label"))
	vb = a.add_child(WidgetController(layout=QVBoxLayout()))
	tf = vb.add_child(TextFieldController())
	tf.set_placeholder("input domain or ip")
	tf.set_label("host")
	tf = vb.add_child(TextFieldController())
	tf.set_placeholder("input ssh port")
	tf.set_label("port")
	tf = vb.add_child(TextFieldController())
	tf.set_placeholder("input user")
	tf.set_label("user")
	tf = vb.add_child(TextFieldController())
	tf.set_placeholder("input password")
	tf.set_label("password")

	stack.widget.resize(800, 640)
	stack.widget.show()

	timer = QTimer()
	timer.setInterval(16)
	timer.timeout.connect(root_ctrl.process_events)
	timer.start()

	sys.exit(app.exec())


if __name__ == "__main__":
	main()
