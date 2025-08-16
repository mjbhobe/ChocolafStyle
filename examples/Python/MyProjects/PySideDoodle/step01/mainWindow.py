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
import PySide6
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

WIN_TITLE = f"PySide {PySide6.__version__} Doodle - Step01: Basic Window"


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle(WIN_TITLE)
        # resize window to use 4/5 of the screen
        self.resize(QGuiApplication.primaryScreen().availableSize() * 4 / 5)
