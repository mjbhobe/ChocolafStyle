"""
// ============================================================================
// step03.py: drawing in the main window
//     application handles the left & right mouse click Events & close event
//       - left mouse click: displays the client co-ordinates where clicked
//       - right mouse click: clears the drawing canvas
//
// Tutorial - PyQt5 Doodle Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// @author: Manish Bhobe
// My experiments with the Qt Framework. Use at your own risk!!
// ============================================================================
"""

import sys
import chocolaf
from mainWindow import *


def main():
    chocolaf.enable_hi_dpi()
    app = chocolaf.ChocolafApp(sys.argv)
    app.setStyle("WindowsDark")

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
