# -*- coding: utf-8 -*-
"""
// ============================================================================
// mainWindow.py: custom QMainWindow derived class for main window
//
// Tutorial - PyQt5 Doodle Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// @author: Manish Bhobe
// My experiments with the Qt Framework. Use at your own risk!!
// ============================================================================
"""
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from drawWindow import DrawWindow
from doodle import Doodle


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(QMainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("PyQt5 Doodle - Step07: Separating the Squiggle Implementation")
        #self.setGeometry(QRect(100, 100, 640, 480))
        self.resize(QGuiApplication.primaryScreen().availableSize() * 4 / 5)
        self.drawWindow = DrawWindow()
        self.setCentralWidget(self.drawWindow)

    # operating system Events
    def closeEvent(self, e):
        """ called just before the main window closes """
        if self.drawWindow.doodle.modified:
            resp = QMessageBox.question(self, "Confirm Close",
                                        "This will close the application.\nOk to quit?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if resp == QMessageBox.Yes:
                e.accept()
            else:
                e.ignore()
        else:
            e.accept()
