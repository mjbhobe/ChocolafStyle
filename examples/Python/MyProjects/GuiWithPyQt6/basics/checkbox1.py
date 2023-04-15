# -*- coding: utf-8 -*-
"""
* checkbox1.py - using a checkbox
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
HOME_DIR = str(pathlib.Path.home())
Window_Title = f"PyQt {PYQT_VERSION_STR} - QCheckbox"


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(Window_Title)
        self.label = QLabel("QCheckbox example")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.checkbox = QCheckBox("This is a checkbox")
        self.checkbox.stateChanged.connect(self.show_checkbox_state)
        self.setupUi()

    def setupUi(self):
        win = QWidget()
        # win.setFixedSize(400, 50)
        layout = QVBoxLayout()
        layout.addWidget(self.checkbox)
        layout.addWidget(self.label)
        win.setLayout(layout)
        self.setCentralWidget(win)

    def show_checkbox_state(self, s):
        self.label.setText(f"The checkbox is {'checked' if Qt.CheckState(s) == Qt.CheckState.Checked else 'unchecked'}")


# app = QApplication(sys.argv)
app = chocolaf.ChocolafApp(sys.argv)
app.setStyle("Chocolaf")

# here is the window
win = MainWindow()
win.show()
sys.exit(app.exec())
