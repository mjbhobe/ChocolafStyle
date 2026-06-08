"""
// ============================================================================
// step02.py: handling events in the main window
//      the main window responds to left & right mouse clicks in the client
//      area with message boxes and also the close event from OS
//
// Tutorial - PyQt5 Doodle Application
// Based on a similar tutorial for Borland(R) ObjectWindows(TM) Library (OWL)
// @author: Manish Bhobé
// My experiments with the Qt Framework. Use at your own risk!!
// ============================================================================
"""

import sys
import platform

import qtpy

from mainWindow import *


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    print(
        f"PyQt Doodle - running with Python {platform.python_version()}, "
        + f"Qt {qtpy.QT_VERSION}, PyQt {qtpy.PYQT_VERSION} on {platform.system()}"
    )

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
