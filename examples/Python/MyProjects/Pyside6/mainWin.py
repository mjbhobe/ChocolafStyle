# This Python file uses the following encoding: utf-8
""" using QMainWindow as main window of application """
import sys
import argparse

from PySide6.QtCore import qVersion
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
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

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--zoom",
        type=float,
        default=1.0,
        help="Zoom level for the font size (default=1.0, no zoom)",
    )
    args = parser.parse_args()
    font = app.font()
    # print(f"Default font: {font.family()}, {font.pointSize()} points", flush=True)
    font.setPointSize(int(font.pointSize() * args.zoom))
    # print(f"Zoomed font: {font.family()}, {font.pointSize()} points", flush=True)
    app.setFont(font)

    # Create GUI
    win = createGui()
    win.show()

    sys.exit(app.exec())
