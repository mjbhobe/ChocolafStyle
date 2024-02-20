"""
// ============================================================================
// step01.py: creating the basic Doodle PyQt application
//
// Tutorial - PyQt5 Doodle Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// @author: Manish Bhobe
// My experiments with the Qt Framework. Use at your own risk!!
// ============================================================================
"""
import platform

import chocolaf
from mainWindow import *

# code to import Chocolaf theme files
from chocolaf.palettes import ChocolafPalette

# from chocolaf.cv2_utils.chocolafapp import ChocolafApp
from chocolaf import ChocolafApp, enable_hi_dpi

__version__ = "1.0"


def main():
    # ChocolafApp.setupAppForHighDpiScreens()
    chocolaf.enable_hi_dpi()
    # app = ChocolafApp(sys.argv)
    # app.setStyle("WindowsDark")
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    print(
        f"PyQt Doodle - running with Python {platform.python_version()}, "
        + f"Qt {QT_VERSION_STR}, PyQt {PYQT_VERSION_STR} on {platform.system()}"
    )

    mainWindow = MainWindow()
    mainWindow.show()

    return app.exec()


if __name__ == "__main__":
    main()
