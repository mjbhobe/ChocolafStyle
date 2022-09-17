#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
* tabWidget.py - using QTabWidget
* @author: Manish Bhobe
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

# Creating the main window


class TabWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super(TabWidget, self).__init__(parent)
        tabWidget = self.createItemViewTabWidget()

        layout = QVBoxLayout()
        layout.addWidget(tabWidget)
        self.setLayout(layout)
        self.setWindowTitle("QTabWidget Demo")

    def embedIntoHBoxLayout(self, widget: QWidget, margin: int = 5) -> QWidget:
        ret = QWidget()
        layout = QHBoxLayout(ret)
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.addWidget(widget)
        return ret

    def createItemViewTabWidget(self) -> QTabWidget:
        result = QTabWidget()
        result.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)

        treeView = QTreeView()
        fileSystemModel = QFileSystemModel(treeView)
        fileSystemModel.setRootPath(QDir.rootPath())
        treeView.setModel(fileSystemModel)

        tableWidget = QTableWidget()
        tableWidget.setRowCount(50)
        tableWidget.setColumnCount(30)

        listModel = QStandardItemModel(0, 1, result)
        dirOpenIcon = QIcon(":/qt-project.org/styles/commonstyle/images/diropen-128.png")
        computerIcon = QIcon(":/qt-project.org/styles/commonstyle/images/computer-32.png")

        listModel.appendRow(QStandardItem(dirOpenIcon, "Directory"))
        listModel.appendRow(QStandardItem(computerIcon, "Compute"))

        listView = QListView()
        listView.setModel(listModel)

        iconModelListView = QListView()
        iconModelListView.setViewMode(QListView.IconMode)
        iconModelListView.setModel(listModel)

        result.addTab(self.embedIntoHBoxLayout(treeView), "&Tree View")
        result.addTab(self.embedIntoHBoxLayout(tableWidget), "T&able")
        result.addTab(self.embedIntoHBoxLayout(listView), "&List")
        result.addTab(self.embedIntoHBoxLayout(iconModelListView), "&Icon Model List")
        return result


def main():
    app = ChocolafApp(sys.argv)
    app.setStyle("Chocolaf")

    win = TabWidget()
    win.move(200, 200)
    win.resize(640, 480)
    win.show()

    rect = win.geometry()
    win1 = TabWidget()
    win1.setStyleSheet(app.getStyleSheet("QDarkStyle-dark"))
    win1.move(rect.left() + rect.width() + 20, rect.top() + 10)
    win1.resize(640, 480)
    win1.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
