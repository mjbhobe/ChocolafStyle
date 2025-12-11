"""
helloPyQt.py - basic PyQt6 application

@author: Manish Bhobe
My experiments with Python & GUI Development
Code has been shared for learning purposes only!
"""
import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        self.label = QLabel(
            f"Hello World! Welcome to Qt6 program with Python\n"
            f"You are using Qt {QT_VERSION_STR}"
        )
        self.setupUi()


    def setupUi(self):
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec())



