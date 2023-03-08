# -*- coding: utf-8 -*-
"""
* pyqtapp.py - utility QApplication derived class to set various themes
* @author: Manish Bhobe
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""

import sys
import os
import logging
import pathlib

import chocolaf
from chocolaf.palettes import ChocolafPalette, WinDarkPalette
from chocolaf.utilities import get_logger

# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *

from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *

_logger = get_logger(pathlib.Path(__file__).name)


class ChocolafApp(QApplication):
    def __init__(self, *args, **kwargs):
        super(ChocolafApp, self).__init__(*args, **kwargs)
        # Nämostuté - sanskrit word, translating to "May our minds meet"
        self.setOrganizationName(chocolaf.__organization__)
        self.setOrganizationDomain(chocolaf.__org_domain__)

        # map of stylesheets
        self.styles = {}
        self.palettes = {}
        # @NOTE: commenting out this line as it causes problems on Windows High-DPI screens
        # where fonts get scaled to huge sizes!
        # self.setFont(QApplication.font("QMenu"))
        self.loadStyleSheets()

    def getPalette(self) -> QPalette:
        palette = QPalette()
        # @see: https://doc.qt.io/qt-5/qpalette.html
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Window,
                         ChocolafPalette.Window_Color)  # general background color
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText,
                         ChocolafPalette.WindowText_Color)  # general foreground color
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Base,
                         ChocolafPalette.Base_Color)  # background for text entry widgets
        # background color for views with alternating colors
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase,
                         ChocolafPalette.AlternateBase_Color)
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase,
                         ChocolafPalette.ToolTipBase_Color)  # background for tooltips
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipText, ChocolafPalette.ToolTipText_Color)
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Text,
                         ChocolafPalette.Text_Color)  # foreground color to use with Base
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Button,
                         ChocolafPalette.Button_Color)  # pushbutton colors
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText,
                         ChocolafPalette.ButtonText_Color)  # pushbutton's text color
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Link, ChocolafPalette.Link_Color)
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.LinkVisited, ChocolafPalette.LinkVisited_Color)
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight,
                         ChocolafPalette.Highlight_Color)  # highlight color
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.HighlightedText,
                         ChocolafPalette.HighlightedText_Color)
        # colors for disabled elements
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText,
                         ChocolafPalette.Disabled_ButtonText_Color)
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText,
                         ChocolafPalette.Disabled_WindowText_Color)
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, ChocolafPalette.Disabled_Text_Color)
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, ChocolafPalette.Disabled_Light_Color)

        return palette

    def loadStyleSheets(self):
        # load chocolaf
        chocolaf_ss = chocolaf.loadStyleSheet()  # self.loadChocoLaf()
        _logger.info(f"Chocolaf stylesheet loaded successfully")
        self.styles["Chocolaf"] = chocolaf_ss
        # self.palettes["Chocolaf"] = self.getPalette()

        try:
            import qdarkstyle
            from qdarkstyle.dark.palette import DarkPalette
            from qdarkstyle.light.palette import LightPalette

            qdarkstyle_darkss = qdarkstyle.load_stylesheet(palette=DarkPalette)
            _logger.info(f"QDarkStyle - dark stylesheet loaded successfully")
            qdarkstyle_darkss += "\nQPushButton{min-height:1.2em; min-width:3em}"
            self.styles["QDarkStyle-dark"] = qdarkstyle_darkss

            qdarkstyle_lightss = qdarkstyle.load_stylesheet(palette=LightPalette)
            _logger.info(f"QDarkStyle - light stylesheet loaded successfully")
            qdarkstyle_lightss += "\nQPushButton{min-height:1.2em; min-width:3em}"
            self.styles["QDarkStyle-light"] = qdarkstyle_lightss

            # NOTE: following styles do not have supporting custom stylesheets
            # self.styles["fusion"] = ""
            # self.styles["windows"] = ""

        except ImportError:
            # if user has not install QDarkStyle, these stylesheets will not be available!
            _logger.info(f"NOTE: QDarkstyle is not available ChocolafApp.setStyle(\"QDarkStyle-XXX\") won't work!")
            pass

    def availableStyles(self, subset='all') -> list:
        assert subset in ['all', 'mine']
        availableStyles = []
        for key in self.styles.keys():
            availableStyles.append(key)
        if subset == 'all':
            # add styles included with PyQt
            for key in QStyleFactory.keys():
                availableStyles.append(key)
        return availableStyles

    def getStyleSheet(self, style: str):
        if style in self.availableStyles('mine'):
            return self.styles[style]
        else:
            availableStyles = self.availableStyles('mine')
            msg = f"\"{style}\" is not recognized as a valid stylesheet!\nValid options are: {availableStyles}"
            raise ValueError(msg)

    def setWindowsDarkStyle(self):
        self.setStyle("Fusion")
        self.setFont(QApplication.font("QMenu"))
        palette = QPalette()
        # @see: https://doc.qt.io/qt-5/qpalette.html
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Window,
                         WinDarkPalette.Window_Color)  # general background color
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText,
                         WinDarkPalette.WindowText_Color)  # general foreground color
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Base,
                         WinDarkPalette.Base_Color)  # background for text entry widgets
        # background color for views with alternating colors
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase,
                         WinDarkPalette.AlternateBase_Color)
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase,
                         WinDarkPalette.ToolTipBase_Color)  # background for tooltips
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipText, WinDarkPalette.ToolTipText_Color)
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Text,
                         WinDarkPalette.Text_Color)  # foreground color to use with Base
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Button,
                         WinDarkPalette.Button_Color)  # pushbutton colors
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText,
                         WinDarkPalette.ButtonText_Color)  # pushbutton's text color
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Link, WinDarkPalette.Link_Color)
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.LinkVisited, WinDarkPalette.LinkVisited_Color)
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight,
                         WinDarkPalette.Highlight_Color)  # highlight color
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.HighlightedText,
                         WinDarkPalette.HighlightedText_Color)
        # colors for disabled elements
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText,
                         WinDarkPalette.Disabled_ButtonText_Color)
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText,
                         WinDarkPalette.Disabled_WindowText_Color)
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, WinDarkPalette.Disabled_Text_Color)
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, WinDarkPalette.Disabled_Light_Color)

        self.setPalette(palette)
        self.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: "
                           "1px solid white; }")

    def setStyle(self, style: str) -> None:
        """ NOTE: style is case sensitive! """
        if style in self.styles.keys():
            stylesheet = self.styles[style]
            # return self.styles[style]
            self.setStyleSheet(stylesheet)
            if style == "Chocolaf":
                self.setPalette(self.getPalette())
        elif style == "WindowsDark":
            self.setWindowsDarkStyle()
        elif style in QStyleFactory.keys():
            super(ChocolafApp, self).setStyle(style)
        else:
            availableStyles = self.availableStyles('all')
            msg = f"\"{style}\" is not recognized as a valid style!\nValid options are: [{availableStyles}]"
            raise ValueError(msg)

    @staticmethod
    def setupAppForHighDpiScreens():
        """ enables scaling for high DPI screens """
        from qtpy import QtCore
        from qtpy.QtWidgets import QApplication
        if sys.platform == "win32":
            # Windows only
            # @see: https://vicrucann.github.io/tutorials/osg-qt-high-dpi/
            # @see: https://stackoverflow.com/questions/44398075/can-dpi-scaling-be-enabled-disabled-programmatically-on-a-per-session-basis
            import ctypes
            # 0 - unaware, 1 - system dpi aware, 2 - per monitor DPI aware
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
            QApplication.setAttribute(QtCore.Qt.AA_DisableHighDpiScaling, True)
            QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
        else:
            if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
                QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

            if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
                QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
