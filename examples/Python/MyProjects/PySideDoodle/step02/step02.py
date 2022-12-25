"""
// ============================================================================
// step02.py: handling events in the main window
//      the main window responds to left & right mouse clicks in the client
//      area with message boxes and also the close event from OS
//
// Tutorial - PySide6 Doodle Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// @author: Manish Bhobe
// My experiments with the Qt Framework. Use at your own risk!!
// ============================================================================
"""
import sys
import platform
import pathlib

# import PySide6
# from PySide6.QtCore import *
# from PySide6.QtGui import *
# from PySide6.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from mainWindow import *

# print(f"You are here: {pathlib.Path(__file__).resolve()}")
# print(f"Your parent is: {pathlib.Path(__file__).resolve().parent}")
# print(f"Your grand-parent is: {pathlib.Path(__file__).resolve().parent.parent}")
sys.path.insert(0, pathlib.Path(__file__).resolve().parent.parent.__str__())
# print(sys.path)
from pyside_doodle import setupAppForHighDpiScreens
# sys.exit(-1)

#from chocolaf.palettes import ChocolafPalette
#from chocolaf.utils.chocolafapp import ChocolafApp


def main():
    setupAppForHighDpiScreens()
    # print(f"PySide Doodle - running with Python {platform.python_version()}, " +
    #       f"Qt {PySide6.QtCore.__version__}, PySide {PySide6.__version__} on {platform.system()}")
    app = QApplication(sys.argv)
    app.setFont(QApplication.font("QMenu"))
    app.setStyle("Fusion")

    mainWindow = MainWindow()
    mainWindow.setFont(QApplication.font("QMenu"))
    mainWindow.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
