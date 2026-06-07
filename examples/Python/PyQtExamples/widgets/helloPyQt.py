"""
helloPyQt.py - basic PyQt6 application

@author: Manish Bhobe
My experiments with Python & GUI Development
Code has been shared for learning purposes only!
"""

import sys
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

import chocolaf


class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super(MainWindow, self).__init__(parent)
        self.label = QLabel(
            f"Hello World! Welcome to GUI programming with Python and Qt\n"
            f"You are using PyQt {PYQT_VERSION_STR}"
        )
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} - Hello World")
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # chocolaf.enable_hi_dpi()
    # app = chocolaf.ChocolafApp(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec())
