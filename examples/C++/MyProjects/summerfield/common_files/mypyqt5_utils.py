#!/usr/bin/env python
# -*- coding: utf-8 -*-
# utils.py - utility functions

import platform
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# using qdarkstyle (@see: https://github.com/ColinDuquesnoy/QDarkStyleSheet)
import qdarkstyle
# to detect dark themes (@see: https://pypi.org/project/darkdetect/)
import darkdetect

__version__ = "1.0"


def getPaletteColor(colorRole: QPalette.ColorRole, colorGroup: QPalette.ColorGroup = QPalette.Active) -> QColor:
    pal = qApp.palette()
    color = pal.color(colorGroup, colorRole)
    return color


def setDarkPalette(app: QApplication, setDark=True) -> None:
    # Dark palette based on Windows 10 dark theme
    # @see for example: https://stackoverflow.com/questions/48256772/dark-theme-for-qt-widgets

    # set dark palette on Windows only
    if platform.platform() == 'Windows':
        if setDark:
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
            palette.setColor(QPalette.Base, QColor(42, 42, 42))
            palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, QColor(53, 53, 53))
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
            palette.setColor(QPalette.Dark, QColor(35, 35, 35))
            palette.setColor(QPalette.Shadow, QColor(20, 20, 20))
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
            palette.setColor(QPalette.HighlightedText, Qt.white)
            palette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127))
            app.setPalette(palette)
        else:
            # does this work?
            app.setStyle("")


class PaletteSwitcher(QObject):
    def __init__(self, appInstance: QApplication, parent: QObject = None):
        super(PaletteSwitcher, self).__init__(parent)
        self.appInstance = appInstance
        self.darkPalette = None
        self.lightPalette = None
        self.darkPaletteInUse = False
        self.__initializePalettes()

    def __initializePalettes(self):
        """ initialize colors for light & dark palettes on Windows - does NOTHING on other platforms """
        self.darkPalette = QPalette()
        self.darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
        self.darkPalette.setColor(QPalette.WindowText, Qt.white)
        self.darkPalette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
        self.darkPalette.setColor(QPalette.Base, QColor(42, 42, 42))
        self.darkPalette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        self.darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
        self.darkPalette.setColor(QPalette.ToolTipText, QColor(53, 53, 53))
        self.darkPalette.setColor(QPalette.Text, Qt.white)
        self.darkPalette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
        self.darkPalette.setColor(QPalette.Dark, QColor(35, 35, 35))
        self.darkPalette.setColor(QPalette.Shadow, QColor(20, 20, 20))
        self.darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
        self.darkPalette.setColor(QPalette.ButtonText, Qt.white)
        self.darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
        self.darkPalette.setColor(QPalette.BrightText, Qt.red)
        self.darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))
        self.darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        self.darkPalette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
        self.darkPalette.setColor(QPalette.HighlightedText, Qt.white)
        self.darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127))

        self.lightPalette = QPalette()
        self.lightPalette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.lightPalette.setColor(QPalette.WindowText, Qt.black)
        self.lightPalette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(240, 240, 240))
        self.lightPalette.setColor(QPalette.Base, Qt.white)
        self.lightPalette.setColor(QPalette.AlternateBase, QColor(233, 231, 227))
        self.lightPalette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
        self.lightPalette.setColor(QPalette.ToolTipText, Qt.black)
        self.lightPalette.setColor(QPalette.Text, Qt.black)
        self.lightPalette.setColor(QPalette.Disabled, QPalette.Text, QColor(120, 120, 120))
        self.lightPalette.setColor(QPalette.Dark, QColor(160, 160, 160))
        self.lightPalette.setColor(QPalette.Shadow, QColor(105, 105, 105))
        self.lightPalette.setColor(QPalette.Button, QColor(240, 240, 240))
        self.lightPalette.setColor(QPalette.ButtonText, Qt.black)
        self.lightPalette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(78, 78, 78))
        self.lightPalette.setColor(QPalette.BrightText, Qt.white)
        self.lightPalette.setColor(QPalette.Link, QColor(0, 0, 255))
        self.lightPalette.setColor(QPalette.Highlight, QColor(0, 120, 215))
        self.lightPalette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(0, 120, 215))
        self.lightPalette.setColor(QPalette.HighlightedText, Qt.white)
        self.lightPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, Qt.white)

    def setDarkPalette(self) -> None:
        """ sets dark palette """
        self.appInstance.setPalette(self.darkPalette)
        self.darkPaletteInUse = True

    def setLightPalette(self) -> None:
        """ sets light palette """
        self.appInstance.setPalette(self.lightPalette)
        self.darkPaletteInUse = False

    def isDarkPaletteInUse(self) -> bool:
        """ checks if dark or light palette is in use """
        return (self.darkPaletteInUse == True)

    def swapPalettes(self) -> None:
        """ swaps palettes - light to dark or vice-versa """
        if self.darkPaletteInUse:
            self.appInstance.setPalette(self.lightPalette)
        else:
            self.appInstance.setPalette(self.darkPalette)
        self.darkPaletteInUse = not self.darkPaletteInUse


class PalMainWindow(QMainWindow):
    def __init__(self, palSwitcher: PaletteSwitcher):
        super(PalMainWindow, self).__init__()
        self.palSwitcher = palSwitcher
        self.timer = QTimer()
        self.timer.timeout.connect(self.switchPalette)
        self.timer.start(1000)

    def switchPalette(self):
        if (darkdetect.isDark() and (not self.palSwitcher.isDarkPaletteInUse())) \
                or ((not darkdetect.isDark()) and self.palSwitcher.isDarkPaletteInUse()):
            self.palSwitcher.swapPalettes()


class PalWidget(QWidget):
    def __init__(self, palSwitcher: PaletteSwitcher):
        super(PalWidget, self).__init__()
        self.palSwitcher = palSwitcher
        self.timer = QTimer()
        self.timer.timeout.connect(self.switchPalette)
        self.timer.start(1000)

    def switchPalette(self):
        if (darkdetect.isDark() and (not self.palSwitcher.isDarkPaletteInUse())) \
                or ((not darkdetect.isDark()) and self.palSwitcher.isDarkPaletteInUse()):
            self.palSwitcher.swapPalettes()
