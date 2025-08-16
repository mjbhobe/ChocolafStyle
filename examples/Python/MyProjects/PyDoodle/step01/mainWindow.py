"""
// ============================================================================
// mainWindow.py: custom QMainWindow derived class for main window
//
// Tutorial - PyQt5 Doodle Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// @author: Manish Bhobé
// My experiments with the Qt Framework with PyQt. Use at your own risk!!
// ============================================================================
"""

import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle(f"PyQt-{PYQT_VERSION_STR} Doodle - Step01: Basic Window")
        # resize window to use 4/5 of the screen
        self.resize(QGuiApplication.primaryScreen().availableSize() * 4 / 5)
