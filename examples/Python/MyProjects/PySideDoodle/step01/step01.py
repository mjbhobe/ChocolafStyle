"""
// ============================================================================
// step01.py: creating the basic Doodle PyQt application
//
// Tutorial - PySide6 Doodle Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// @author: Manish Bhobe
// My experiments with the Qt Framework. Use at your own risk!!
// ============================================================================
"""
import sys
import platform
import PySide6
from PySide6.QtGui import *
from PySide6.QtGui import *
from mainWindow import *

# code to import Chocolaf theme files
# from chocolaf.palettes import ChocolafPalette
# from chocolaf.utils.chocolafapp import Chocolaf

__version__ = "1.0"


def main():
    app = QApplication(sys.argv)
    print(f"PySide Doodle - running with Python {platform.python_version()}, " +
          f"Qt {PySide6.QtCore.__version__}, PySide {PySide6.__version__} on {platform.system()}")

    mainWindow = MainWindow()
    mainWindow.show()

    return app.exec()


if __name__ == "__main__":
    main()
