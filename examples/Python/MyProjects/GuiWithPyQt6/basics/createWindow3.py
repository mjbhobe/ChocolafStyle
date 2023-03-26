# -*- coding: utf-8 -*-
"""
* createWindow3.py - using QMainWindow of fixed size
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

import chocolaf

APP_PATH = os.path.dirname(__file__)
Window_Title = f"PyQt {PYQT_VERSION_STR} - Create basic window"
HOME_DIR = str(pathlib.Path.home())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(Window_Title)
        self.button = QPushButton(chocolaf.get_icon("Cancel"), "Click Me")
        self.button.clicked.connect(QApplication.instance().quit)
        self.setCentralWidget(self.button)
        self.setFixedSize(QSize(400, 300))


# app = QApplication(sys.argv)
app = chocolaf.ChocolafApp(sys.argv)
app.setStyle("WindowsDark")

# here is the window
win = MainWindow()
win.show()
sys.exit(app.exec())
