#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
* listWidget.py - illustrates simple use of the QListWidget class
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

class ListWidgetWindow(QWidget):
    def __init__(self, parent: QWidget=None):
        super(ListWidgetWindow, self).__init__(parent)
        self.listWidget = QListWidget()
        self.button = QPushButton("Change Selected Item")
        self.setupUi()
        self.button.clicked.connect(self.changeListWidgetItem)

    def setupUi(self):
        for i in range(25):
            self.listWidget.addItem(f"List Widget Item {i:02d}")
        layout = QVBoxLayout()
        layout.addWidget(self.listWidget)
        layout.addWidget(self.button)
        self.setLayout(layout)
    
    def changeListWidgetItem(self):
        item : QListWidgetItem = self.listWidget.currentItem()
        if item:
            item.setForeground(Qt.magenta)
            item.setBackground(Qt.blue)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = ListWidgetWindow()
    win.show()

    sys.exit(app.exec())
        