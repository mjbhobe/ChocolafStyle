#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
* frames.py - illustrates various styles of QFrame class
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
        label = QLabel("Box")
        label1 = QLabel("Panel")
        label2 = QLabel("Winpanel")
        label3 = QLabel("H line")
        label4 = QLabel("V line")
        label5 = QLabel("Styled Panel")

        label.setFrameStyle(QFrame.Box or QFrame.Raised)
        label.setLineWidth(2)
        label1.setFrameStyle(QFrame.Panel or QFrame.Raised)
        label1.setLineWidth(2)
        label2.setFrameStyle(QFrame.WinPanel or QFrame.Raised)
        label2.setLineWidth(2)
        label3.setFrameStyle(QFrame.HLine or QFrame.Raised)
        label3.setLineWidth(2)
        label4.setFrameStyle(QFrame.VLine or QFrame.Raised)
        label4.setLineWidth(2)
        label5.setFrameStyle(QFrame.StyledPanel or QFrame.Sunken)
        label5.setLineWidth(2)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        layout.addWidget(label4)
        layout.addWidget(label5)
        self.setLayout(layout)
        self.setWindowTitle("QFrame Demo")


def main():
    app = ChocolafApp(sys.argv)
    app.setStyle("QDarkStyle-dark")

    w = Form()
    # w.setStyleSheet(app.getStyleSheet("Chocolaf"))
    w.move(100, 100)
    w.show()

    # rect = w.geometry()
    # w1 = Form()
    # w1.setStyleSheet(app.getStyleSheet("QDarkStyle-dark"))
    # w1.move(rect.left() + rect.width() + 20, rect.top())
    # w1.show()

    # rect = w1.geometry()
    # w2 = Form()
    # w2.setStyleSheet(app.getStyleSheet("QDarkStyle-light"))
    # w2.move(rect.left() + rect.width() + 20, rect.top())
    # w2.show()

    # rect = w2.geometry()
    # w3 = Form()
    # w3.move(rect.left() + rect.width() + 20, rect.top())
    # w3.show()

    return app.exec()


if __name__ == "__main__":
    main()
