#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
* sigslots.py - illustrates signals & slots with PyQt with a QDial & 
*    QSpinBox class using Chocolaf & QarkStyle-dark stylesheets
* @author: Manish Bhobe
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import os
import pathlib
import sys

from PyQt5.QtWidgets import *

from chocolaf.utils.chocolafapp import ChocolafApp


class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()

        self.dial = QDial()
        self.dial.setNotchesVisible(True)
        self.spinBox = QSpinBox()
        self.spinBox2 = QSpinBox()
        self.spinBox2.setEnabled(False)

        spinLayout = QVBoxLayout()
        spinLayout.addStretch()
        spinLayout.addWidget(self.spinBox)
        spinLayout.addWidget(self.spinBox2)
        spinLayout.addStretch()

        layout = QHBoxLayout()
        layout.addWidget(self.dial)
        # layout.addWidget(self.spinBox)
        layout.addLayout(spinLayout)

        self.pb = QPushButton("Quit")
        self.pb.setDefault(True)
        self.pb.clicked.connect(qApp.quit)

        layout2 = QHBoxLayout()
        layout2.addStretch()
        layout2.addWidget(self.pb)

        # vlayout = QVBoxLayout()
        # vlayout.addLayout(layout)
        # vlayout.addLayout(layout2)

        self.setLayout(layout)

        # connect valueChanged signals to each other
        self.dial.valueChanged.connect(self.spinBox.setValue)
        self.spinBox.valueChanged.connect(self.dial.setValue)
        self.resize(350, 200)
        self.setWindowTitle("Qt Signals & Slots Demo")


def main():
    app = ChocolafApp(sys.argv)

    w = Form()
    w.setStyleSheet(app.getStyleSheet("Chocolaf"))
    w.move(100, 100)
    w.setWindowTitle(f"{w.windowTitle()} - using Chocolaf")
    w.show()

    rect = w.geometry()
    w1 = Form()
    w1.setStyleSheet(app.getStyleSheet("QDarkStyle-dark"))
    w1.setWindowTitle(f"{w1.windowTitle()} - using QDarkStyle-dark")
    w1.move(rect.left() + rect.width() + 50, rect.top() + rect.height() // 4 + 50)
    w1.show()

    rect = w1.geometry()
    w2 = Form()
    w2.setStyleSheet(app.getStyleSheet("QDarkStyle-light"))
    w2.setWindowTitle(f"{w1.windowTitle()} - using QDarkStyle-light")
    w2.move(rect.left() + rect.width() + 50, rect.top() + rect.height() // 4 + 50)
    w2.show()

    return app.exec()


if __name__ == "__main__":
    main()
