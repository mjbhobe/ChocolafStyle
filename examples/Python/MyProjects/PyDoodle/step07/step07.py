# -*- coding: utf-8 -*-
"""
// ===================================================================================
// step07.py: drawing multiple squiggles in window, each with own attribute
//  application handles left mouse press & drag, right mouse press events
//   - draws a squiggle in the client window when left mouse is pressed & dragged
//   - if ctrl + left mouse press - display dialog to set new pen thickness
//   - if ctrl + right mouse press - display dialog to set new pen thickness
//     (NOTE: Ctrl + mouse clicks is perhaps not the best way to design a GUI.
//      We are using this method as we have not yet introduces menus & toolbars.
//      This flaw will be corrected in steps where these GUI elements are introduced)
//
// Tutorial - PyQt5 Doodle Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// @author: Manish Bhobe
// My experiments with the Qt Framework. Use at your own risk!!
// =====================================================================================
"""
import sys

import chocolaf
from mainWindow import MainWindow


def main():
    chocolaf.enable_hi_dpi()
    app = chocolaf.ChocolafApp(sys.argv)
    app.setStyle("WindowsDark")

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
