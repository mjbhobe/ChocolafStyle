# -*- coding: utf-8 -*-
"""
* sigSlot.py - basic signals & slots
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

        self.setWindowTitle(f"Signals & Slots with PyQt {PYQT_VERSION_STR}")
        self.setFixedSize(400, 150)
        button = QPushButton("Click Me!")
        button.setCheckable(True)
        # setup slot for clicked signal
        button.clicked.connect(self.button_clicked)
        # since button is checked, this is handler for "checked" on/off
        button.clicked.connect(self.button_toggled)
        # set it as the main window
        self.setCentralWidget(button)

    def button_clicked(self):
        # just print a message
        print("Button was clicked!")

    def button_toggled(self, checked):
        # show state - Checked? True/False
        print(f"Checked? {checked}")

app = QApplication(sys.argv)
win = MainWindow()
win.show()

sys.exit(app.exec())