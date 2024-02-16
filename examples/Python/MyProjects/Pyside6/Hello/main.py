# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtCore import qVersion
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout

def createGui():
  win: QWidget = QWidget()
  label: QLabel = QLabel(f"Hello, welcome to PySide {qVersion()}")
  layout: QVBoxLayout = QVBoxLayout()
  layout.addWidget(label)
  win.setLayout(layout)
  win.setWindowTitle("Hello PySide")
  win.setMinimumWidth(480)
  return win


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # ...
    win = createGui()
    win.show()

    sys.exit(app.exec())
