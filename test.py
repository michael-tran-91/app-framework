from PySide6.QtWidgets import QApplication, QPushButton
import sys

app = QApplication(sys.argv)

button = QPushButton("Gradient Border")

button.setStyleSheet("""
QPushButton {
    color: black;
    background-color: white;
    border: 3px solid transparent;
    border-radius: 8px;
    padding: 6px 12px;

    /* Gradient border trick */
    background-clip: padding-box;
}

QPushButton {
    border-image: none;
    border: 3px solid transparent;
    border-radius: 8px;
    background-origin: border-box;
    background-clip: content-box, border-box;
    background-image: linear-gradient(white, white),
                      linear-gradient(45deg, #ff0000, #0000ff);
}
""")

button.show()
sys.exit(app.exec())
