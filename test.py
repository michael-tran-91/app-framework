# qlineedit_top_edge.py
import sys
from html import unescape
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QTextEdit
)
from PySide6.QtCore import Qt, QObject, QEvent, QRect
from PySide6.QtGui import QIcon

# User's Edge browser tabs metadata
edge_all_open_tabs = [
    {"pageTitle":"<WebsiteContent_3UxP9pmMaCWTtcW3qCAy8>Using PyInstaller \u2014 PyInstaller 6.20.0 documentation</WebsiteContent_3UxP9pmMaCWTtcW3qCAy8>",
     "pageUrl":"<WebsiteContent_3UxP9pmMaCWTtcW3qCAy8>https://pyinstaller.org/en/stable/usage.html?utm_source=copilot.com</WebsiteContent_3UxP9pmMaCWTtcW3qCAy8>",
     "tabId":1889614328,"isCurrent":True}
]

def get_current_tab(tabs):
    return next((t for t in tabs if t.get("isCurrent")), None)

class TopOverlayLabel(QLabel):
    """Overlay label pinned to the top edge of its parent."""
    def __init__(self, text: str = "", parent: QWidget | None = None,
                 left_margin: int = 0, right_margin: int = 0, accept_mouse: bool = False):
        super().__init__(text, parent)
        self._left_margin = left_margin
        self._right_margin = right_margin
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setStyleSheet("""
            background: rgba(255,255,255,0.95);
            border-bottom: 1px solid #ddd;
            padding: 6px 10px;
            font-weight: 600;
            color: #111;
        """)
        if not accept_mouse:
            self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        if parent is not None:
            parent.installEventFilter(self)
            self.raise_()
            self._update_geometry()

    def set_margins(self, left: int, right: int):
        self._left_margin = left
        self._right_margin = right
        self._update_geometry()

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj is self.parent() and event.type() in (QEvent.Resize, QEvent.LayoutRequest):
            self._update_geometry()
        return super().eventFilter(obj, event)

    def _parent_inner_width(self) -> int:
        p = self.parent()
        if p is None:
            return self.width()
        return max(0, p.width() - (self._left_margin + self._right_margin))

    def _update_geometry(self):
        p = self.parent()
        if p is None:
            return
        avail_w = self._parent_inner_width()
        x = self._left_margin
        h = self.sizeHint().height()
        y = -h / 2.0
        self.setGeometry(QRect(x, y, avail_w, h))
        self.raise_()

    def setText(self, text: str):
        super().setText(text)
        self.setFixedHeight(self.sizeHint().height())
        self._update_geometry()

class TabEditorWidget(QWidget):
    def __init__(self, tabs):
        super().__init__()
        self.tabs = tabs
        self.current = get_current_tab(tabs)

        self.setWindowTitle("QLineEdit with Top Edge Label")
        self.resize(800, 420)

        # central layout and content
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)

        # content area to demonstrate overlay behavior
        content = QTextEdit()
        content.setPlainText("Main content area\n" * 30)
        main_layout.addWidget(content)

        # editable title field and read-only URL placed in a bottom dock area
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(8)

        self.title_field = QLineEdit()
        self.title_field.setPlaceholderText("Current tab title")
        self.title_field.setClearButtonEnabled(True)
        self.title_field.setObjectName("currentTitleField")
        self.title_field.setStyleSheet("QLineEdit { color: #000000; padding: 6px; border-radius: 6px; }")
        if self.current:
            self.title_field.setText(unescape(self.current.get("pageTitle", "")))
        bottom_row.addWidget(self.title_field, stretch=2)

        self.url_field = QLineEdit()
        self.url_field.setReadOnly(True)
        self.url_field.setObjectName("urlField")
        self.url_field.setStyleSheet("QLineEdit { color: #000000; padding: 6px; border-radius: 6px; }")
        if self.current:
            self.url_field.setText(unescape(self.current.get("pageUrl", "")))
        bottom_row.addWidget(self.url_field, stretch=3)

        copy_btn = QPushButton("Copy URL")
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(self.url_field.text()))
        bottom_row.addWidget(copy_btn)

        main_layout.addLayout(bottom_row)

        # create overlay label pinned to top edge of this widget
        title_text = unescape(self.current.get("pageTitle", "")) if self.current else "No current tab"
        self.top_label = TopOverlayLabel("abc", parent=self.title_field, left_margin=12, right_margin=12, accept_mouse=False)

        # optional: update overlay when title_field changes
        self.title_field.editingFinished.connect(self._on_title_changed)

    def _on_title_changed(self):
        new_title = self.title_field.text().strip()
        # update overlay label text (safe: we only display text)
        self.top_label.setText(new_title)
        # update internal metadata if present
        if self.current is not None:
            self.current["pageTitle"] = new_title

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TabEditorWidget(edge_all_open_tabs)
    w.show()
    sys.exit(app.exec())
