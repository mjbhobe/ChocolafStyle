"""
// ============================================================================
// step02.py: handling events in the main window
//      the main window responds to left & right mouse clicks in the client
//      area with message boxes and also the close event from OS
//
// Tutorial - PyQt5 Doodle Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// @author: Manish Bhobe
// My experiments with the Qt Framework. Use at your own risk!!
// ============================================================================
"""
import sys
import platform

import chocolaf
from mainWindow import *


def main():
    chocolaf.enable_hi_dpi()
    print(
        f"PyQt Doodle - running with Python {platform.python_version()}, "
        + f"Qt {QT_VERSION_STR}, PyQt {PYQT_VERSION_STR} on {platform.system()}"
    )
    # app = chocolaf.ChocolafApp(sys.argv)
    # app.setStyle("WindowsDark")
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
