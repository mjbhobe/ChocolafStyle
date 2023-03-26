# -*- coding: utf-8 -*-
"""
* simpleTableView.py - displays a simple read-only table view
*   with 5 rows & 6 cols
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
Window_Title = f"PyQt {PYQT_VERSION_STR} MVC - Simple QTableView"
HOME_DIR = str(pathlib.Path.home())


# define the model
class MyModel(QAbstractTableModel):
    def __init__(self):
        super(MyModel, self).__init__()
        self.num_rows = 10
        self.num_cols = 6

    # must define the following 3 funcs
    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self.num_rows

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return self.num_cols

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return f"Row: {index.row()} Col: {index.column()}"
        else:
            return QVariant()


def main():
    app = chocolaf.ChocolafApp(sys.argv)
    app.setStyle("WindowsDark")

    # setup the GUI
    win = QMainWindow()
    win.setWindowTitle(Window_Title)

    tableView = QTableView()
    model = MyModel()
    tableView.setModel(model)
    win.setCentralWidget(tableView)
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
