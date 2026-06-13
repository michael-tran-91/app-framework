"""PySide6 palette demo.

Run:
	python main.py

Shows application palettes, role swatches, and a widget-level palette.
"""

import sys
from PySide6.QtWidgets import (
	QApplication,
	QWidget,
	QLabel,
	QVBoxLayout,
	QHBoxLayout,
	QPushButton,
	QLineEdit,
	QTextEdit,
	QGridLayout,
	QGroupBox,
	QFrame,
	QComboBox,
)
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt


def create_dark_palette(accent=QColor("#528bff")):
	p = QPalette()
	p.setColor(QPalette.Window, QColor("#282c34"))
	p.setColor(QPalette.WindowText, QColor("#abb2bf"))
	p.setColor(QPalette.Base, QColor("#21252b"))
	p.setColor(QPalette.AlternateBase, QColor("#2b2f34"))
	p.setColor(QPalette.ToolTipBase, QColor("#f5f5b5"))
	p.setColor(QPalette.ToolTipText, QColor("#000000"))
	p.setColor(QPalette.Text, QColor("#abb2bf"))
	p.setColor(QPalette.Button, QColor("#3e4451"))
	p.setColor(QPalette.ButtonText, QColor("#dcdfe4"))
	p.setColor(QPalette.BrightText, QColor("#ff5555"))
	p.setColor(QPalette.Link, accent)
	p.setColor(QPalette.Highlight, accent)
	p.setColor(QPalette.HighlightedText, QColor("#ffffff"))
	return p


def create_light_palette(accent=QColor("#0066cc")):
	p = QPalette()
	p.setColor(QPalette.Window, QColor("#f0f0f0"))
	p.setColor(QPalette.WindowText, QColor("#222222"))
	p.setColor(QPalette.Base, QColor("#ffffff"))
	p.setColor(QPalette.AlternateBase, QColor("#e6e6e6"))
	p.setColor(QPalette.ToolTipBase, QColor("#ffffdc"))
	p.setColor(QPalette.ToolTipText, QColor("#000000"))
	p.setColor(QPalette.Text, QColor("#222222"))
	p.setColor(QPalette.Button, QColor("#efefef"))
	p.setColor(QPalette.ButtonText, QColor("#222222"))
	p.setColor(QPalette.BrightText, QColor("#e81123"))
	p.setColor(QPalette.Link, accent)
	p.setColor(QPalette.Highlight, accent)
	p.setColor(QPalette.HighlightedText, QColor("#ffffff"))
	return p


def get_roles():
	roles = [
		("Window", QPalette.Window),
		("WindowText", QPalette.WindowText),
		("Base", QPalette.Base),
		("Text", QPalette.Text),
		("Button", QPalette.Button),
		("ButtonText", QPalette.ButtonText),
		("Highlight", QPalette.Highlight),
		("HighlightedText", QPalette.HighlightedText),
		("Link", QPalette.Link),
		("ToolTipBase", QPalette.ToolTipBase),
		("ToolTipText", QPalette.ToolTipText),
		("AlternateBase", QPalette.AlternateBase),
	]
	if hasattr(QPalette, "PlaceholderText"):
		roles.append(("PlaceholderText", QPalette.PlaceholderText))
	return roles


class PaletteDemo(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("PySide6 Palette Demo")
		self.resize(800, 600)

		self.original_palette = QApplication.palette()
		self.app = QApplication.instance()

		main_layout = QVBoxLayout(self)

		# Controls
		ctrl_layout = QHBoxLayout()
		self.palette_combo = QComboBox()
		self.palette_combo.addItems(["System", "Dark", "Light"])
		self.palette_combo.currentTextChanged.connect(self.on_palette_change)

		ctrl_layout.addWidget(QLabel("Palette:"))
		ctrl_layout.addWidget(self.palette_combo)
		ctrl_layout.addStretch()
		main_layout.addLayout(ctrl_layout)

		# Role swatches
		swatch_box = QGroupBox("Palette Role Swatches")
		swatch_layout = QGridLayout()
		self.swatches = {}
		roles = get_roles()
		for idx, (name, role) in enumerate(roles):
			sw = self._make_swatch(name, role)
			r = idx // 3
			c = idx % 3
			swatch_layout.addWidget(sw, r, c)
		swatch_box.setLayout(swatch_layout)
		main_layout.addWidget(swatch_box)

		# Example widgets that use the application's palette
		demo_box = QGroupBox("Widgets Using the Palette")
		demo_layout = QHBoxLayout()

		left_col = QVBoxLayout()
		left_col.addWidget(QLabel("QLineEdit (Base/Text):"))
		self.line = QLineEdit()
		self.line.setPlaceholderText("Placeholder text shows PlaceholderText role")
		left_col.addWidget(self.line)

		left_col.addWidget(QLabel("QTextEdit (Base/Text):"))
		self.text = QTextEdit()
		self.text.setPlaceholderText("This is a QTextEdit.")
		left_col.addWidget(self.text)

		demo_layout.addLayout(left_col)

		right_col = QVBoxLayout()
		self.button = QPushButton("Primary Button")
		right_col.addWidget(self.button)
		disabled_btn = QPushButton("Disabled Button")
		disabled_btn.setEnabled(False)
		right_col.addWidget(disabled_btn)

		# A widget with its own palette
		self.widget_groupbox = QGroupBox("Widget-level Palette")
		wp_layout = QVBoxLayout()
		self.widget_demo = QLabel("This groupbox uses a custom light palette")
		self.widget_demo.setAlignment(Qt.AlignCenter)
		wp_layout.addWidget(self.widget_demo)
		self.widget_groupbox.setLayout(wp_layout)

		right_col.addWidget(self.widget_groupbox)
		demo_layout.addLayout(right_col)

		demo_box.setLayout(demo_layout)
		main_layout.addWidget(demo_box)

		# Actions
		actions = QHBoxLayout()
		apply_widget_btn = QPushButton("Apply Light Palette To Group")
		apply_widget_btn.clicked.connect(self.apply_widget_palette)
		restore_btn = QPushButton("Restore System Palette")
		restore_btn.clicked.connect(self.restore_system_palette)
		actions.addWidget(apply_widget_btn)
		actions.addWidget(restore_btn)
		actions.addStretch()
		main_layout.addLayout(actions)

		# initialize to System
		self.palette_combo.setCurrentText("System")
		self.on_palette_change(self.palette_combo.currentText())

	def _make_swatch(self, name, role):
		container = QWidget()
		h = QHBoxLayout(container)
		h.setContentsMargins(6, 6, 6, 6)
		frame = QFrame()
		frame.setFixedSize(64, 28)
		label = QLabel(name)
		label.setAlignment(Qt.AlignCenter)
		h.addWidget(frame)
		h.addWidget(label)
		# store references for updates
		self.swatches[role] = {"frame": frame, "label": label, "name": name}
		return container

	def update_swatches(self, palette: QPalette):
		for role, info in self.swatches.items():
			frame = info["frame"]
			label = info["label"]
			name = info["name"]
			color = palette.color(role)
			hexc = color.name()
			frame.setStyleSheet(f"background-color: {hexc}; border: 1px solid #444;")
			label.setText(f"{name}\n{hexc}")

	def on_palette_change(self, text):
		if text == "Dark":
			p = create_dark_palette()
			self.app.setPalette(p)
		elif text == "Light":
			p = create_light_palette()
			self.app.setPalette(p)
		else:
			self.app.setPalette(self.original_palette)

		# Update the widget demo to reflect palette changes
		current = self.app.palette()
		self.update_swatches(current)

	def apply_widget_palette(self):
		# Apply a light palette to the groupbox/widget_demo only
		p = create_light_palette(QColor("#aa5500"))
		self.widget_groupbox.setAutoFillBackground(True)
		wpal = QPalette()
		wpal.setColor(QPalette.Window, p.color(QPalette.Window))
		wpal.setColor(QPalette.WindowText, p.color(QPalette.WindowText))
		self.widget_groupbox.setPalette(wpal)

	def restore_system_palette(self):
		self.palette_combo.setCurrentText("System")
		self.app.setPalette(self.original_palette)
		self.update_swatches(self.original_palette)


def main():
	app = QApplication(sys.argv)
	demo = PaletteDemo()
	demo.show()
	sys.exit(app.exec())


if __name__ == "__main__":
	main()
