import sys

from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)


class TitleBar(QWidget):
    def __init__(self, window):
        super().__init__()

        self.window = window
        self.drag_pos = QPoint()

        self.setFixedHeight(36)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)

        title = QLabel("My App")

        layout.addWidget(title)
        layout.addStretch()

        btn_min = QPushButton("—")
        btn_close = QPushButton("✕")

        btn_min.setFixedSize(30, 24)
        btn_close.setFixedSize(30, 24)

        btn_min.clicked.connect(window.showMinimized)
        btn_close.clicked.connect(window.close)

        layout.addWidget(btn_min)
        layout.addWidget(btn_close)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = (
                event.globalPosition().toPoint()
                - self.window.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.window.move(
                event.globalPosition().toPoint()
                - self.drag_pos
            )


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.Window | Qt.FramelessWindowHint
        )

        self.resize(600, 400)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(TitleBar(self))

        content = QLabel("Content Area")
        content.setAlignment(Qt.AlignCenter)

        layout.addWidget(content)

        self.setStyleSheet("""
            QWidget {
                background: white;
            }

            TitleBar {
                background: #f0f0f0;
            }

            QPushButton {
                border: none;
                padding: 4px;
            }

            QPushButton:hover {
                background: #dddddd;
            }
        """)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()