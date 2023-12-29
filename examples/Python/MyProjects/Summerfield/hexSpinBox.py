#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
* hexspinBox.py: customized spinbox displaying hexadecimal numbers
* @author (Chocolaf): Manish Bhobe
*
* PyQt demo code taken from https://github.com/baoboa/pyqt5/tree/master/examples/widgets
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import chocolaf
from chocolaf.utils.chocolafapp import ChocolafApp


class HexSpinBox(QSpinBox):
    def __init__(self, parent: QWidget = None):
        super(HexSpinBox, self).__init__(parent)
        self.setRange(0, 65535)  # FFFF
        # allow upto 8 chars from {0-9} or {A-F} or {a-f}
        self.validator = QRegExpValidator(QRegExp("[0-9A-Fa-f]{1,8}"))

    def validate(self, text: str, pos: int):
        return self.validator.validate(text, pos)

    def textFromValue(self, value: int) -> str:
        try:
            return f"{hex(value)}"
        except TypeError as err:
            raise (err)

    def valueFromText(self, text: str) -> int:
        try:
            return int(text, 16)
        except ValueError as err:
            raise (err)


def main():
    # app = ChocolafApp(sys.argv)
    # app.setStyle("Chocolaf")
    ChocolafApp.setupAppForHighDpiScreens()
    app = ChocolafApp(sys.argv)
    app.setStyle("Fusion")

    # create & show GUI
    win = QWidget()
    layout = QGridLayout()
    label = QLabel("Hex Spinbox:")
    hexSpinBox = HexSpinBox()
    closeBtn = QPushButton("Close")
    hexSpinBox.setValue(1247)
    layout.addWidget(label, 0, 0)
    layout.addWidget(hexSpinBox, 0, 1)
    layout.addWidget(closeBtn, 1, 1)
    win.setLayout(layout)
    closeBtn.clicked.connect(app.exit)
    closeBtn.setDefault(True)
    win.setWindowTitle("Custom SpinBox")
    win.setMinimumWidth(220)
    win.show()

    return app.exec()


if __name__ == "__main__":
    main()
