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
        self.setRange(0, 255)
        # allow upto 8 chars from {0-9} or {A-F} or {a-f}
        self.validator = QRegExpValidator(QRegExp("[0-9A-Fa-f]{1,8}"))

    def validate(self, text: str, pos:int) -> QValidator.State:
        return self.validator.validate(text, pos)

    def textFromValue(self, value:int) -> str:
        try:
            return f"{hex(value)}"
        except TypeError as err:
            raise(err)

    def valueFromText(self, text:str) -> int:
        try:
            return int(str, 16)
        except ValueError as err:
            raise(err)

def main():
    # app = ChocolafApp(sys.argv)
    # app.setStyle("Chocolaf")
    app = QApplication(sys.argv)

    # create & show GUI
    win = QWidget()
    layout = QHBoxLayout()
    label = QLabel("Hex Spinbox:")
    hexSpinBox = HexSpinBox()
    hexSpinBox.setValue(128)
    layout.addWidget(label)
    layout.addWidget(hexSpinBox)
    win.setLayout(layout)
    win.setWindowTitle("Custom SpinBox")
    win.show()

    return app.exec()


if __name__ == "__main__":
    main()