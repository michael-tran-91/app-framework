import sys
from PySide6.QtWidgets import (
    QApplication, QTableWidget, QPushButton, QCheckBox
)

app = QApplication(sys.argv)

table = QTableWidget()
table.setRowCount(3)
table.setColumnCount(2)
table.setHorizontalHeaderLabels(["Action", "Select"])

# Add a button in the first column
for row in range(3):
    btn = QPushButton(f"Click {row+1}")
    table.setCellWidget(row, 0, btn)

# Add a checkbox in the second column
for row in range(3):
    chk = QCheckBox("Check")
    table.setCellWidget(row, 1, chk)

table.show()
sys.exit(app.exec())
