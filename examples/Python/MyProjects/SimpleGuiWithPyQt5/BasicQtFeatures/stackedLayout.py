"""
* stackedLayout.py: illustrates use of stacked layout
* @author (Chocolaf): Manish Bhobe
*
* Examples from book "Create Simple Gui Applications with Python & Qt5 - Martin Fitzpatrick"
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!
"""

import sys
import os
import random

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# import chocolaf
from chocolaf.utils.chocolafapp import ChocolafApp

app_dir = os.path.dirname(__file__)


class Color(QWidget):
    def __init__(self, color, *args, darken=True, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.color = color
        self.darken = darken
        self.setAutoFillBackground(True)
        palette = self.palette()
        clr = QColor(color)
        if self.darken:
            clr = clr.darker(factor=100)
        palette.setColor(QPalette.Window, clr)
        self.setPalette(palette)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        # @see: https://www.w3schools.com/colors/colors_names.asp
        # self.rainbow = ['violet', 'indigo', 'blue',
        #                 'green', 'yellow', 'orange', 'red']
        self.rainbow = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure',
                        'beige', 'bisque', 'black', 'blanchedalmond',
                        'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue',
                        'chartreuse', 'chocolate', 'coral', 'cornflowerblue']
        self.layout = QStackedLayout()

        for color in self.rainbow:
            self.layout.addWidget(Color(QColor(color)))
        self.setLayout(self.layout)
        self.pick_random_index()

        self.resize(400, 200)
        icon_path = os.path.join(app_dir, "haha.png")
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} random colors")
        self.timer = QTimer()
        self.timer.timeout.connect(self.pick_random_index)
        self.timer.start(1000)  # fire every 2 second

    def pick_random_index(self):
        rand_index = random.randint(0, len(self.rainbow) - 1)
        self.setWindowTitle(
            f"PyQt {PYQT_VERSION_STR} random colors \'{self.rainbow[rand_index]}\'")
        self.layout.setCurrentIndex(rand_index)


app = ChocolafApp(sys.argv)
# app.setStyle("QDarkStyle-dark")

win = Window()
win.show()

app.exec()
