from .widget_controller import WidgetController
from core.controller.controller import Event
from PySide6.QtWidgets import QTableWidget, QSlider, QHeaderView, QTableWidgetItem, QAbstractItemView
from PySide6.QtCore import Qt
from ..widget.animated_scrollbar import AnimatedScrollBar

class TableController(WidgetController):

    def __init__(self):
        super().__init__(layout=None, widget=QTableWidget())
        self.widget.setViewportMargins(0, 0, 50, 0)  # left, top, right, bottom
        self.widget.setProperty("role", "default")
        self.widget.horizontalHeader().setProperty("role", "default")
        self.widget.setShowGrid(False)
        self.widget.horizontalHeader().setFixedHeight(30)
        self.widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.widget.verticalHeader().setVisible(False)
        self.widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        scrollbar = AnimatedScrollBar(Qt.Vertical, self.widget)
        self.widget.setVerticalScrollBar(scrollbar)
        scrollbar.attachTo(self.widget)

        scrollbar = AnimatedScrollBar(Qt.Horizontal, self.widget)
        self.widget.setHorizontalScrollBar(scrollbar)
        scrollbar.attachTo(self.widget)

    def handle_set(self, event: Event):
        super().handle_set(event)

        if "columns" in event.data:
            self.widget.setColumnCount(event.data["columns"])

        if "headers" in event.data:
            self.widget.setHorizontalHeaderLabels(event.data["headers"])

        if "columns_width" in event.data:
            _len = len(event.data["columns_width"])
            for i in range(len(event.data["columns_width"])):
                _w = event.data["columns_width"][i]
                if _w > 0:
                    self.widget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Fixed)
                    self.widget.setColumnWidth(i, _w)
                else:
                    if i < _len - 1:
                        self.widget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Interactive)
                    else:
                        self.widget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

            for i in range(100):
                new_row_index = self.widget.rowCount()
                self.widget.insertRow(new_row_index)
                t = QTableWidgetItem("David")
                t.setFlags(t.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEditable) 
                t.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widget.setItem(new_row_index, 0, t)
                t = QTableWidgetItem("28")
                t.setFlags(t.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEditable) 
                t.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widget.setItem(new_row_index, 1, t)
                t = QTableWidgetItem("Paris")
                t.setFlags(t.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEditable) 
                t.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widget.setItem(new_row_index, 2, t)