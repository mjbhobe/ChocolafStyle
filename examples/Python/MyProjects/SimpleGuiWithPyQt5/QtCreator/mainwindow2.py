# -*- coding: utf-8 -*-
"""
* mainwindow2.py - this example illustrates an alternate way of using
*  *.ui files in your PyQt code.py
*  Steps:
*    1. compile your ui file into a py file using 
*           pyuic5 <ui_file_name> -o <python_file_name>
*    2. import your python module like you would normally
*           import <python_file_name>
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

# NOTE: mainwindow_rc.py was created on the command line using
#   pyuic5 mainwindow.ui -o mainwindow_rc.py
# it creates a class called Ui_MainWindow
from mainwindow_rc import Ui_MainWindow

APP_PATH = os.path.dirname(__file__)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.button_text = f"Welcome to PyQt {PYQT_VERSION_STR}"
        self.label.setText(self.button_text)
        self.pushButton.clicked.connect(self.button_clicked)
        self.click_count = 0

    def button_clicked(self):
        self.click_count += 1
        self.label.setText(f"{self.button_text} - clicked {self.click_count} times")


app = ChocolafApp(sys.argv)
app.setStyle("Chocolaf")
window = MainWindow()  # uic.loadUi(os.path.join(APP_PATH, "mainwindow.ui"))
# setupWindow(window)
window.show()

app.exec()
