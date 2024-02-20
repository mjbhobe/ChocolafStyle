"""
// ================================================================================
// step04.py: drawing a squiggle in the main window
//  application handles left mouse press & drag, right mouse press events
//   - draws a squiggle in the client window when left mouse is pressed & dragged
//   - erases the squiggle when the right mouse is pressed
//
// Tutorial - PyQt5 Doodle Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// @author: Manish Bhobe
// My experiments with the Qt Framework. Use at your own risk!!
// =================================================================================
"""
import sys
from mainWindow import *

import chocolaf


def main():
    chocolaf.enable_hi_dpi()
    # app = ChocolafApp(sys.argv)
    # app.setStyle("WindowsDark")
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
