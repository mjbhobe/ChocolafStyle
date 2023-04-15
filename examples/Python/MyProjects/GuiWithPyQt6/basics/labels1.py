# -*- coding: utf-8 -*-
"""
* labels1.py - display label as central widget
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
Window_Title = f"PyQt {PYQT_VERSION_STR} - Labels"
HOME_DIR = str(pathlib.Path.home())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(Window_Title)
        self.label = QLabel(f"Hello PyQt {PYQT_VERSION_STR}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        font = self.label.font()
        font.setPixelSize(32)
        self.label.setFont(font)
        self.setCentralWidget(self.label)


# app = QApplication(sys.argv)
app = chocolaf.ChocolafApp(sys.argv)
app.setStyle("WindowsDark")

# here is the window
win = MainWindow()
win.show()
sys.exit(app.exec())
