# This Python file uses the following encoding: utf-8
""" using QMainWindow as main window of application """
import sys
from PySide6.QtCore import qVersion
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMainWindow
)

def createGui():
    mainWin = QMainWindow()
    win: QWidget = QWidget()
    label: QLabel = QLabel(f"Hello, welcome to PySide {qVersion()}")
    layout: QVBoxLayout = QVBoxLayout()
    layout.addWidget(label)
    win.setLayout(layout)
    mainWin.setWindowTitle("Hello PySide")
    mainWin.setMinimumWidth(480)
    mainWin.setCentralWidget(win)
    return mainWin


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create GUI
    win = createGui()
    win.show()

    sys.exit(app.exec())
