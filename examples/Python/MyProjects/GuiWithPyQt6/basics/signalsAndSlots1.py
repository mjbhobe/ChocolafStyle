# -*- coding: utf-8 -*-
"""
* signalsAndSlots1.py - using signals & slots
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
import qtawesome as qta  # SVG icons

APP_PATH = os.path.dirname(__file__)
Window_Title = f"PyQt {PYQT_VERSION_STR} - Signals & Slots"
HOME_DIR = str(pathlib.Path.home())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.icon_off = qta.icon("ei.bullhorn")
        self.icon_on = qta.icon("ph.smiley-wink-fill", color="#EBCB8B")
        self.button1 = QPushButton(self.icon_off, "Click Me")
        self.button1.setCheckable(True)
        self.button2 = QPushButton(chocolaf.get_icon("Cancel"), "Close")
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle(Window_Title)
        win = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        win.setLayout(layout)
        self.setCentralWidget(win)
        self.setFixedSize(QSize(300, 100))
        # setup signals & slots
        self.button1.clicked.connect(self.button_clicked)
        self.button2.clicked.connect(QApplication.instance().quit)

    def button_clicked(self):
        self.button1.setIcon(
            self.icon_on if self.button1.isChecked()
            else self.icon_off
        )
        self.button1.setText(
            "You Clicked Me!" if self.button1.isChecked() else "Click Me"
        )


# app = QApplication(sys.argv)
app = chocolaf.ChocolafApp(sys.argv)
app.setStyle("WindowsDark")
# app.setStyle("Fusion")

# here is the window
win = MainWindow()
win.show()
sys.exit(app.exec())
