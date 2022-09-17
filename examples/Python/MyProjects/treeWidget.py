#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
* treeWidget.py - using the QTreeWidget
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

class TreeWidgetWindow(QWidget):
    def __init__(self, parent: QWidget=None):
        super(TreeWidgetWindow, self).__init__(parent)
        self.treeWidget = QTreeWidget()
        self.setupUi()

    def setupUi(self):
        self.treeWidget.setColumnCount(2)
        self.addTreeRoot("A", "Root_first")
        self.addTreeRoot("B", "Root_second")
        self.addTreeRoot("C", "Root_third")
        layout = QVBoxLayout()
        layout.addWidget(self.treeWidget)
        self.setLayout(layout)

    def addTreeRoot(self, name, description):
        treeItem = QTreeWidgetItem(self.treeWidget)
        treeItem.setText(0, name)
        treeItem.setText(1, description)
        self.addTreeChild(treeItem, f"{name}A", "Child_first")
        self.addTreeChild(treeItem, f"{name}B", "Child_second")

    def addTreeChild(self, parent, name, description):
        treeItem = QTreeWidgetItem()
        treeItem.setText(0, name)
        treeItem.setText(1, description)
        parent.addChild(treeItem)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    win = TreeWidgetWindow()
    win.show()

    sys.exit(app.exec())
        