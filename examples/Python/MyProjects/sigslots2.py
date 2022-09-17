#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
* sigslots2.py - many to 1 signal handler using QPushButtons
*   and Chocolaf & QDarkStyle-dark, QDarkStyle-light and Fusion stylesheets
* @author: Manish Bhobe
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import sys

from PyQt5.QtWidgets import *

from chocolaf.utils.chocolafapp import ChocolafApp


class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()
        texts = ["One", "Two", "Three", "Four", "Five"]
        layout = QHBoxLayout()
        for text in texts:
            button = QPushButton(text)
            button.clicked.connect(self.btnClicked)
            layout.addWidget(button)
        closeBtn = QPushButton("Close")
        closeBtn.setDefault(True)
        closeBtn.clicked.connect(qApp.exit)
        self.label = QLabel("Which button clicked?")
        layout.addWidget(self.label)
        self.setLayout(layout)
        layout.addWidget(closeBtn)
        self.setWindowTitle("Qt Signals & Slots Demo")

    def btnClicked(self):
        button = self.sender()
        self.label.setText(f"You clicked {button.text()}")


def main():
    app = ChocolafApp(sys.argv)
    app.setStyle("Fusion")

    w = Form()
    w.setStyleSheet(app.getStyleSheet("Chocolaf"))
    w.setWindowTitle(f"{w.windowTitle()} - using Chocolaf")
    w.move(100, 100)
    w.show()

    rect = w.geometry()
    w1 = Form()
    w1.setStyleSheet(app.getStyleSheet("QDarkStyle-dark"))
    w1.setWindowTitle(f"{w1.windowTitle()} - using QDarkStyle-dark")
    w1.move(rect.left() + 20, rect.top() + rect.height() + 50)
    w1.show()

    rect = w1.geometry()
    w2 = Form()
    w2.setStyleSheet(app.getStyleSheet("QDarkStyle-light"))
    w2.setWindowTitle(f"{w2.windowTitle()} - using QDarkStyle-light")
    w2.move(rect.left() + 20, rect.top() + rect.height() + 50)
    w2.show()

    rect = w2.geometry()
    w3 = Form()
    w3.move(rect.left() + 20, rect.top() + rect.height() + 50)
    w3.setWindowTitle(f"{w3.windowTitle()} - using Fusion")
    w3.show()

    return app.exec()


if __name__ == "__main__":
    main()
