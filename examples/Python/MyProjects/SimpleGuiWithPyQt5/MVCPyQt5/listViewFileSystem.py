# -*- coding: utf-8 -*-
"""
* listViewFileSystem.py - display file system using QListView & QTreeView
*
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!

"""
import sys
import os
import pathlib

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from chocolaf.palettes import ChocolafPalette
from chocolaf.utils.chocolafapp import ChocolafApp

APP_PATH = os.path.dirname(__file__)
Window_Title = f"PyQt {PYQT_VERSION_STR} MVC - 2 views of same file system"
HOME_DIR = str(pathlib.Path.home())

if __name__ == "__main__":
    app = ChocolafApp(sys.argv)
    # app.setStyle("Chocolaf")

    splitter = QSplitter()
    splitter.setMinimumSize(800, 400)
    model = QFileSystemModel()
    model.setRootPath("/")

    # set splitter views
    tree = QTreeView(splitter)
    tree.setModel(model)
    tree.setRootIndex(model.index(HOME_DIR))

    list = QListView(splitter)
    list.setModel(model)
    list.setRootIndex(model.index(HOME_DIR))

    splitter.setWindowTitle("Two views onto the same file system model")
    w = splitter.size().width()
    # splitter.setSizes([0.6 * splitter.width(), 0.4 * splitter.width()])
    splitter.setSizes([int(0.7 * w), int(0.3 * w)])
    splitter.show()

    sys.exit(app.exec())