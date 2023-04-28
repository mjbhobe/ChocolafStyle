# -*- coding: utf-8 -*-
"""
* simpleTableWidget.py - displays data using QTableWidget
*
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!

"""
import sys
import os
import pathlib
import typing

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import uic

import chocolaf

APP_PATH = os.path.dirname(__file__)
Window_Title = f"PyQt {PYQT_VERSION_STR} - using QTableWidget"
HOME_DIR = str(pathlib.Path.home())

colors = [("Red", "#FF0000"),
          ("Green", "#00FF00"),
          ("Blue", "#0000FF"),
          ("Black", "#000000"),
          ("White", "#FFFFFF"),
          ("Electric Green", "#41CD52"),
          ("Dark Blue", "#222840"),
          ("Yellow", "#F9E56d")]


def get_rgb_from_hex(code):
    code_hex = code.replace("#", "")
    rgb = tuple(int(code_hex[i:i + 2], 16) for i in (0, 2, 4))
    return QColor.fromRgb(rgb[0], rgb[1], rgb[2])


def main():
    app = chocolaf.ChocolafApp(sys.argv)
    app.setStyle("WindowsDark")

    # create & show GUI
    table = QTableWidget()
    table.setRowCount(len(colors))
    table.setColumnCount(len(colors[0]) + 1)
    table.setHorizontalHeaderLabels(["Name", "Hex Code", "Color"])
    table.setWindowTitle(Window_Title)

    for i, (name, code) in enumerate(colors):
        item_name = QTableWidgetItem(name)
        item_code = QTableWidgetItem(code)
        item_color = QTableWidgetItem()
        item_color.setBackground(get_rgb_from_hex(code))
        table.setItem(i, 0, item_name)
        table.setItem(i, 1, item_code)
        table.setItem(i, 2, item_color)

    table.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
