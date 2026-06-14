import sys
from PySide6.QtWidgets import (QApplication, QSizePolicy, QVBoxLayout, QHBoxLayout)
from PySide6.QtCore import QTimer
from core.controller.controller import Event
from core.controller.root_controller import RootController
from graphic.controller.widget_controller import WidgetController
from graphic.controller.shadow_edge_controller import ShadowEdgeController
from graphic.controller.stacked_controller import StackedController
from graphic.controller.splitter_controller import SplitterController
from graphic.controller.button_controller import ButtonController
from graphic.controller.toggle_controller import ToggleController
from graphic.controller.label_controller import LabelController
from graphic.controller.notched_text_field_controller import NotchedTextFieldController
from graphic.controller.text_field_controller import TextFieldController
from graphic.controller.table_controller import TableController
from PySide6.QtCore import Qt
from util.file_manager import fetch as fetch_file_content

light_styleSheet = fetch_file_content(path="app://res/theme/light.qss", encoding="utf8")
dark_styleSheet = fetch_file_content(path="app://res/theme/dark.qss", encoding="utf8")

class AppWidget(WidgetController):

	def __init__(self, app:QApplication):
		super().__init__(layout=QVBoxLayout())
		self._app = app

	def handle_light_dark(self, event: Event):
		if event.data["checked"]:
			self._app.setStyleSheet(light_styleSheet)
		else:
			self._app.setStyleSheet(dark_styleSheet)

	def _on_attached(self):
		super()._on_attached()
		stack = self.add_child(StackedController())
		stack.dispatch_event(Event(event_type="set", data={
			"role" : "main_background"
		}))
		splitter = stack.add_child(SplitterController(orientation=Qt.Horizontal))

		widget = splitter.add_child(WidgetController(layout=QVBoxLayout()))
		shadow = widget.add_child(ShadowEdgeController(layout=QVBoxLayout()))
		shadow.dispatch_event(Event(event_type="set", data={
			"side" : ShadowEdgeController.TOP | ShadowEdgeController.BOTTOM | ShadowEdgeController.LEFT
		}))
		a = shadow.add_child(WidgetController(layout=QVBoxLayout()))
		a.dispatch_event(Event(event_type="set", data={
			"role" : "test_widget"
		}))
		tblc = a.add_child(TableController())
		tblc.dispatch_event(Event(event_type="set", data={
			"columns": 3,
			"headers" : ["adress", "class name", "function name"],
			"columns_width" : [100, -1, -1]
		}))

		widget = splitter.add_child(WidgetController(layout=QVBoxLayout()))
		shadow = widget.add_child(ShadowEdgeController(layout=QVBoxLayout()))
		shadow.dispatch_event(Event(event_type="set", data={
			"content_margins" : [6, 6, 0, 0]
		}))

		shadow.dispatch_event(Event(event_type="set", data={
			"side" : ShadowEdgeController.TOP | ShadowEdgeController.RIGHT | ShadowEdgeController.BOTTOM | ShadowEdgeController.LEFT
		}))
		a = shadow.add_child(WidgetController(layout=QVBoxLayout()))
		a.dispatch_event(Event(event_type="set", data={
			"role" : "test_widget2",
			"spacing" : 10,
			"size_policy" : ["expanding", "maximum"]
		}))
		btn = a.add_child(ButtonController())
		btn.dispatch_event(Event(event_type="set", data={
			"width" : 100,
			"height" : 40
		}))

		btn = a.add_child(ToggleController(True))
		btn.dispatch_event(Event(event_type="set", data={
			"role" : "toggle_theme",
			"width" : 60,
			"height" : 30
		}))
		self.light_dark_toggle = btn

		a = shadow.add_child(WidgetController(layout=QHBoxLayout()))
		self.lb = a.add_child(LabelController("Test Label"))
		self.lb.dispatch_event(Event(event_type="set", data={
			"text" : "Hello world"
		}), reuse_context=True)
		a.add_child(LabelController("Test Label"))
		vb = a.add_child(WidgetController(layout=QVBoxLayout()))
		vb.dispatch_event(Event(event_type="set", data={
			"spacing" : 10
		}))
		tf = vb.add_child(NotchedTextFieldController())
		tf.dispatch_event(Event(event_type="set", data={
			"placeholder" : "input domain or ip",
			"label" : "host",
			"width" : 300
		}))
		tf = vb.add_child(NotchedTextFieldController())
		tf.dispatch_event(Event(event_type="set", data={
			"placeholder" : "input ssh port",
			"label" : "port",
			"width" : 300
		}))
		tf = vb.add_child(NotchedTextFieldController())
		tf.dispatch_event(Event(event_type="set", data={
			"placeholder" : "input user",
			"label" : "user",
			"width" : 300
		}))
		tf = vb.add_child(TextFieldController())
		tf.dispatch_event(Event(event_type="set", data={
			"placeholder" : "input password",
			"label" : "password",
			"width" : 300
		}))
		tblc = vb.add_child(TableController())
		tblc.dispatch_event(Event(event_type="set", data={
			"columns": 3,
			"headers" : ["adress", "class name", "function name"],
			"columns_width" : [100, -1, -1]
		}))

		self.register_event_handler("toggle_controller_clicked", self.handle_light_dark, required_controllers=[
			self.light_dark_toggle
		])


def main():
	app = QApplication(sys.argv)
	app.setStyleSheet(light_styleSheet)

	root = RootController()
	app_widget = root.add_child(AppWidget(app))
	app_widget.widget.resize(800, 640)
	app_widget.widget.show()
	timer = QTimer()
	timer.setInterval(16)
	timer.timeout.connect(root.process_events)
	timer.start()

	sys.exit(app.exec())


if __name__ == "__main__":
	main()
