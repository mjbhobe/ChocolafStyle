"""
// ============================================================================
// step02.py: handling events in the main window
//      the main window responds to left & right mouse clicks in the client
//      area with message boxes and also the close event from OS
//
// Tutorial - PySide6 Doodle Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// @author: Manish Bhobé
// My experiments with the Qt Framework. Use at your own risk!!
// ============================================================================
"""

import os

os.environ["QT_API"] = "pyqt5"

import sys
import platform
import pathlib

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *
from mainWindow import *

import chocolaf


def main():
    chocolaf.enable_hi_dpi()
    app = chocolaf.ChocolafApp(sys.argv)
    app.setStyle("Fusion")
    # print(f"PySide Doodle - running with Python {platform.python_version()}, " +
    #       f"Qt {PySide6.QtCore.__version__}, PySide {PySide6.__version__} on {platform.system()}")

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
