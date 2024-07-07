# -*- coding: utf-8 -*-
"""
* firstApp.py: basic application with PyQt6
*
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import sys
import os
import pathlib

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"Hello Python {PYQT_VERSION_STR}")
        self.setFixedSize(400, 150)
        button = QPushButton("Click Me!")
        # set it as the main window
        self.setCentralWidget(button)

app = QApplication(sys.argv)
win = MainWindow()
win.show()

sys.exit(app.exec())