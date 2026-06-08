"""
// ============================================================================
// step01.py: creating the basic Doodle PyQt application
//
// Tutorial - PyQt5 Doodle Application
// Based on a similar tutorial for Borland(R) ObjectWindows(TM) Library (OWL)
// @author: Manish Bhobé
// My experiments with the Qt Framework. Use at your own risk!!
// ============================================================================
"""

import platform

import qtpy

from mainWindow import *

__version__ = "1.0"


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    print(
        f"PyQt Doodle - running with Python {platform.python_version()}, "
        + f"Qt {qtpy.QT_VERSION}, PyQt {qtpy.PYQT_VERSION} on {platform.system()}"
    )

    mainWindow = MainWindow()
    mainWindow.show()

    return app.exec()


if __name__ == "__main__":
    main()
