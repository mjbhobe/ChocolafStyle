""" test.py - create the basic PyQt6 application """
import sys

from PyQt6.QtCore import PYQT_VERSION_STR
import PyQt6.QtWidgets


def main():
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    # create the main window
    win = PyQt6.QtWidgets.QWidget()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
