"""
* color.py - a color widget in a VBoxLayout
* @author (Chocolaf): Manish Bhobe
*
* Examples from book "Create Simple Gui Applications with Python & Qt5 - Martin Fitzpatrick"
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!
"""

import sys
import os

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import chocolaf

app_dir = os.path.dirname(__file__)


class Color(QWidget):
    def __init__(self, color, *args, darken = True, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.color = color
        self.darken = darken
        self.setAutoFillBackground(True)
        palette = self.palette()
        clr = QColor(color)
        if self.darken:
            clr = clr.darker(factor = 150)
        palette.setColor(QPalette.Window, clr)
        self.setPalette(palette)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        rainbow = ['violet', 'indigo', 'blue',
                   'green', 'yellow', 'orange', 'red']
        layout = QHBoxLayout()  # QVBoxLayout()
        layout.setSpacing(0)
        for color in rainbow:
            layout.addWidget(Color(QColor(color), darken = False))
        self.setLayout(layout)

        self.resize(300, 300)
        icon_path = os.path.join(app_dir, "images", "avatar1.png")
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} rainbow")


chocolaf.enable_hi_dpi()
app = chocolaf.ChocolafApp(sys.argv)
# app.setStyle("Chocolaf")
app.setStyle("WindowsDark")

win = Window()
win.show()

app.exec()
