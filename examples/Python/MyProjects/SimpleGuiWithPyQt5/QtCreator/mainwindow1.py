# -*- coding: utf-8 -*-
"""
* mainwindow1.py - this example illustrates how to load a *.ui file
*  created in Qt Designer/Creator into your Python code & customizing it
* @author (Chocolaf): Manish Bhobe
*
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!

"""
import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from chocolaf.palettes import ChocolafPalette
from chocolaf.utils.chocolafapp import ChocolafApp

APP_PATH = os.path.dirname(__file__)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # load the ui file - this behaves like a Qt Widget
        self.ui = uic.loadUi(os.path.join(APP_PATH, "mainwindow.ui"))
        self.ui.pushButton.clicked.connect(self.button_clicked)
        self.button_text = f"Welcome to PyQt {PYQT_VERSION_STR}"
        self.ui.label.setText(self.button_text)
        self.click_count = 0

    def show(self):
        self.ui.show()

    def button_clicked(self):
        self.click_count += 1
        self.ui.label.setText(f"{self.button_text} - clicked {self.click_count} times")


def setupWindow(window):
    window.setWindowTitle(f"PyQt {PYQT_VERSION_STR} MainWindow")


app = ChocolafApp(sys.argv)
app.setStyle("Chocolaf")
window = MainWindow()  # uic.loadUi(os.path.join(APP_PATH, "mainwindow.ui"))
# setupWindow(window)
window.show()

app.exec()
