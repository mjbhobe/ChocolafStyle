#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
* RadioGaga.py: demonstrating Radio buttons & Radio groups
* @author: Manish Bhobe
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


class RadioForm(QWidget):
    def __init__(self):
        super(RadioForm, self).__init__()
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        gbox = QGroupBox("T-Shirt Size")
        rb1 = QRadioButton("Large", self)
        rb1.toggled.connect(self.updateLabel)

        rb2 = QRadioButton("Medium", self)
        rb2.toggled.connect(self.updateLabel)

        rb3 = QRadioButton("Small", self)
        rb3.toggled.connect(self.updateLabel)

        self.label = QLabel('', self)

        hbox.addWidget(rb1)
        hbox.addWidget(rb2)
        hbox.addWidget(rb3)
        gbox.setLayout(hbox)

        vbox.addSpacing(15)

        # vbox.addLayout(hbox)
        vbox.addWidget(gbox)
        vbox.addWidget(self.label)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('QRadioButton Example')
        self.show()

    def updateLabel(self, value):
        rbtn = self.sender()

        if rbtn.isChecked() == True:
            self.label.setText(rbtn.text())


class RadioGroupForm(QWidget):
    def __init__(self, parent: QWidget = None):
        super(RadioGroupForm, self).__init__(parent)
        self.initUi()

    def initUi(self):
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()

        bg1 = QButtonGroup(self)

        rb1 = QRadioButton("Large", self)
        rb1.toggled.connect(self.updateLabel1)

        rb2 = QRadioButton("Middle", self)
        rb2.toggled.connect(self.updateLabel1)

        rb3 = QRadioButton("Small", self)
        rb3.toggled.connect(self.updateLabel1)

        hbox2 = QHBoxLayout()
        bg2 = QButtonGroup(self)

        rb4 = QRadioButton("Red", self)
        rb4.toggled.connect(self.updateLabel2)

        rb5 = QRadioButton("Green", self)
        rb5.toggled.connect(self.updateLabel2)

        rb6 = QRadioButton("Blue", self)
        rb6.toggled.connect(self.updateLabel2)

        self.label1 = QLabel('', self)
        self.label2 = QLabel('', self)

        bg1.addButton(rb1)
        bg1.addButton(rb2)
        bg1.addButton(rb3)

        bg2.addButton(rb4)
        bg2.addButton(rb5)
        bg2.addButton(rb6)

        hbox1.addWidget(rb1)
        hbox1.addWidget(rb2)
        hbox1.addWidget(rb3)

        hbox2.addWidget(rb4)
        hbox2.addWidget(rb5)
        hbox2.addWidget(rb6)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.label1)
        vbox.addWidget(self.label2)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('QRadioButton')
        self.show()

    def updateLabel1(self, value):

        rbtn = self.sender()

        if rbtn.isChecked() == True:
            self.label1.setText(rbtn.text())

    def updateLabel2(self, value):

        rbtn = self.sender()

        if rbtn.isChecked() == True:
            self.label2.setText(rbtn.text())


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
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = ChocolafApp(sys.argv)

    w = RadioGroupForm()
    w.setStyleSheet(app.getStyleSheet("Chocolaf"))
    w.move(100, 100)
    w.show()

    rect = w.geometry()
    w1 = RadioGroupForm()
    w1.setStyleSheet(app.getStyleSheet("QDarkStyle-dark"))
    w1.move(rect.left() + rect.width() + 20,
            rect.top() + rect.height() // 4 + 20)
    w1.show()

    return app.exec()


if __name__ == "__main__":
    main()
