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

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import uic

import chocolaf

APP_PATH = os.path.dirname(__file__)
Window_Title = f"PyQt {PYQT_VERSION_STR} MVC - 2 views of same file system"
HOME_DIR = str(pathlib.Path.home())

style_sheet = """
    QTreeView#FileSystemTreeView {
        background: transparent;
        selection-color: #ffffff;
    }
"""

if __name__ == "__main__":
    chocolaf.enable_hi_dpi()
    app = chocolaf.ChocolafApp(sys.argv)
    # app.setStyle("Chocolaf")
    app.setStyle("WindowsDark")

    splitter = QSplitter()
    splitter.setMinimumSize(800, 400)
    model = QFileSystemModel()
    model.setRootPath("/")

    # set splitter views
    tree = QTreeView(splitter)
    tree.setObjectName("FileSystemTreeView")
    tree.setModel(model)
    tree.setRootIndex(model.index(HOME_DIR))

    list = QListView(splitter)
    list.setModel(model)
    list.setRootIndex(model.index(HOME_DIR))

    splitter.setWindowTitle(Window_Title)
    w = splitter.size().width()
    # splitter.setSizes([0.6 * splitter.width(), 0.4 * splitter.width()])
    splitter.setSizes([int(0.7 * w), int(0.3 * w)])
    splitter.setStyleSheet(style_sheet)
    splitter.show()

    sys.exit(app.exec())
