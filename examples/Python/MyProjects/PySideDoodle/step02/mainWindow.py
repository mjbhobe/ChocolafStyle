"""
// ============================================================================
// mainWindow.py: custom QMainWindow derived class for main window
//
// Tutorial - PySide6 Doodle Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// @author: Manish Bhobe
// My experiments with the Qt Framework. Use at your own risk!!
// ============================================================================
"""
import os
import sys

import qtpy
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

WIN_TITLE = f"{qtpy.API_NAME} Doodle - Step02: Handling Events"


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(WIN_TITLE)
        self.messageLabel = QLabel(
            "Left or Right click anywhere inside the client area of window", parent = self
        )
        self.messageLabel.setGeometry(10, 5, 500, 50)
        self.resize(QGuiApplication.primaryScreen().availableSize() * 4 / 5)

    # operating system Events
    def closeEvent(self, e: QCloseEvent) -> None:
        resp = QMessageBox.question(
            self, "Confirm Close",
            "This will close the application.\nOk to quit?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
        if resp == QMessageBox.Yes:
            e.accept()
        else:
            e.ignore()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.LeftButton:
            QMessageBox.information(
                self, "PyQt Doodle",
                "You have pressed the LEFT mouse clostBtn"
            )
        elif e.button() == Qt.RightButton:
            QMessageBox.information(
                self, "PyQt Doodle",
                "You have pressed the RIGHT mouse clostBtn"
            )
