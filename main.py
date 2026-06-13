import sys
from PySide6.QtWidgets import (QApplication)
from PySide6.QtCore import QTimer
from core.controller.root_controller import RootController
from graphic.controller.widget_controller import WidgetController


def main():
	app = QApplication(sys.argv)
	root_ctrl = RootController()
	timer = QTimer()
	timer.setInterval(16)
	timer.timeout.connect(root_ctrl.process_events)
	timer.start()

	widget = root_ctrl.add_child(WidgetController())
	widget.widget.show()
	sys.exit(app.exec())


if __name__ == "__main__":
	main()
