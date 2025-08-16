#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
* interestCalc.py: compound interest calculator exercise
* @author: Manish Bhobé
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import os
import pathlib
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from chocolaf.utils.chocolafapp import ChocolafApp


class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()
        self.label1 = QLabel("Principal:")
        self.principal = QSpinBox()
        self.label2 = QLabel("Rate:")
        self.rate = QDoubleSpinBox()
        self.label3 = QLabel("Years:")
        self.years = QComboBox()
        self.label4 = QLabel("Amount:")
        self.interest = QLabel("Final Amount")
        self.label4 = QLabel("Amount:")
        self.amount = QLabel("Final Amount")
        self.sizeGrip = QSizeGrip(self)
        self.setupUi()

    def setupUi(self):
        self.principal.setPrefix("$")
        self.principal.setRange(1000, 100000)
        self.principal.setSingleStep(500)
        self.principal.setValue(2000)
        self.label2 = QLabel("Rate:")
        self.rate = QDoubleSpinBox()
        self.rate.setSuffix("%")
        self.rate.setRange(0.01, 10.00)
        self.rate.setSingleStep(0.05)
        self.rate.setValue(5.25)
        self.label3 = QLabel("Years:")
        for i in range(1, 26):
            self.years.addItem(f"{i} years")
        self.years.setCurrentIndex(1)

        # layout in grid layout
        layout = QGridLayout()
        layout.addWidget(self.label1, 0, 0)
        layout.addWidget(self.principal, 0, 1)
        layout.addWidget(self.label2, 1, 0)
        layout.addWidget(self.rate, 1, 1)
        layout.addWidget(self.label3, 2, 0)
        layout.addWidget(self.years, 2, 1)
        layout.addWidget(self.label4, 3, 0)
        layout.addWidget(self.amount, 3, 1)
        self.setLayout(layout)

        # connect signals & slots
        self.principal.valueChanged.connect(self.calcInterest)
        self.rate.valueChanged.connect(self.calcInterest)
        self.years.currentIndexChanged.connect(self.calcInterest)
        # display initial calculation
        self.calcInterest()

        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} interest calculator")
        self.setMinimumSize(250, 50)

    def calcInterest(self):
        p = float(self.principal.value())
        r = float(self.rate.value())
        y = self.years.currentIndex() + 1
        a = p * ((1 + (r / 100.0)) ** y)
        self.amount.setText(f"$ {a:.2f}")


def loadStyleSheet() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    print(f"loasStyleSteet() -> You are {here}")
    darkss_dir = os.path.join(here, "styles", "dark")
    sys.path.append(darkss_dir)
    import stylesheet_rc

    darkss_path = os.path.join(darkss_dir, "stylesheet.css")
    assert os.path.exists(darkss_path)
    print(f"LoasStyleSheet() -> loading dark stylesheet from {darkss_path}")
    stylesheet = ""
    with open(darkss_path, "r") as f:
        stylesheet = f.read()
    return stylesheet


def main():
    ChocolafApp.setupAppForHighDpiScreens()
    app = ChocolafApp(sys.argv)

    w = Form()
    w.move(500, 100)
    w.show()

    rect = w.geometry()
    w1 = Form()
    w1.setStyleSheet(app.getStyleSheet("Chocolaf"))
    w1.move(rect.left() + rect.width() + 20, rect.top() + rect.height() // 4 + 20)
    w1.show()

    rect = w1.geometry()
    w2 = Form()
    w2.setStyleSheet(app.getStyleSheet("QDarkStyle-dark"))
    w2.move(rect.left() + rect.width() + 20, rect.top() + rect.height() // 4 + 20)
    w2.show()

    return app.exec()


if __name__ == "__main__":
    main()
