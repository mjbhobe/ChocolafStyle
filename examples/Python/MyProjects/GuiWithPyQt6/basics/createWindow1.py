# -*- coding: utf-8 -*-
"""
* createWindow1.py - create &  a simple PyQt6 window
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

# app = QApplication(sys.argv)
app = chocolaf.ChocolafApp(sys.argv)
app.setStyle("WindowsDark")

# here is the window
win = QWidget()
win.setWindowTitle(Window_Title)
win.show()
sys.exit(app.exec())
