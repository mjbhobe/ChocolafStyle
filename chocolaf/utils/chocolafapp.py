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
import chocolaf
from chocolaf.palettes import ChocolafPalette

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ChocolafApp(QApplication):
    def __init__(self, *args, **kwargs):
        super(ChocolafApp, self).__init__(*args, **kwargs)
        # Nämostuté - sanskrit word, tranlating to "May our minds meet"
        self.setOrganizationName("Nämostuté Ltd.")
        self.setOrganizationDomain("namostute.qtpyapps.in")

        # map of stylesheets
        self.styles = {}
        self.palettes = {}
        #self.font = QFont("")
        self.setFont(QApplication.font("QMenu"))
        self.loadStyleSheets()

    def getPalette(self) -> QPalette:
        palette = QPalette()
        # @see: https://doc.qt.io/qt-5/qpalette.html
        palette.setColor(QPalette.Window, ChocolafPalette.Window_Color)         # general background color
        palette.setColor(QPalette.WindowText, ChocolafPalette.WindowText_Color)  # general foreground color
        palette.setColor(QPalette.Base, ChocolafPalette.Base_Color)        # background for text entry widgets
        # background color for views with alternating colors
        palette.setColor(QPalette.AlternateBase, ChocolafPalette.AlternateBase_Color)
        palette.setColor(QPalette.ToolTipBase, ChocolafPalette.ToolTipBase_Color)  # background for tooltips
        palette.setColor(QPalette.ToolTipText, ChocolafPalette.ToolTipText_Color)
        palette.setColor(QPalette.Text, ChocolafPalette.Text_Color)             # foreground color to use with Base
        palette.setColor(QPalette.Button, ChocolafPalette.Button_Color)         # pushbutton colors
        palette.setColor(QPalette.ButtonText, ChocolafPalette.ButtonText_Color)  # pushbutton's text color
        palette.setColor(QPalette.Link, ChocolafPalette.Link_Color)
        palette.setColor(QPalette.LinkVisited, ChocolafPalette.LinkVisited_Color)
        palette.setColor(QPalette.Highlight, ChocolafPalette.Highlight_Color)     # highlight color
        palette.setColor(QPalette.HighlightedText, ChocolafPalette.HighlightedText_Color)
        # colors for disabled elements
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, ChocolafPalette.Disabled_ButtonText_Color)
        palette.setColor(QPalette.Disabled, QPalette.WindowText, ChocolafPalette.Disabled_WindowText_Color)
        palette.setColor(QPalette.Disabled, QPalette.Text, ChocolafPalette.Disabled_Text_Color)
        palette.setColor(QPalette.Disabled, QPalette.Light, ChocolafPalette.Disabled_Light_Color)

        return palette

    def loadStyleSheets(self):
        # load chocolaf
        chocolaf_ss = chocolaf.loadStyleSheet()  # self.loadChocoLaf()
        self.styles["Chocolaf"] = chocolaf_ss
        # self.palettes["Chocolaf"] = self.getPalette()

        try:
            import qdarkstyle
            from qdarkstyle.dark.palette import DarkPalette
            from qdarkstyle.light.palette import LightPalette

            qdarkstyle_darkss = qdarkstyle.load_stylesheet(palette=DarkPalette)
            qdarkstyle_darkss += "\nQPushButton{min-height:1.2em; min-width:3em}"
            self.styles["QDarkStyle-dark"] = qdarkstyle_darkss

            qdarkstyle_lightss = qdarkstyle.load_stylesheet(palette=LightPalette)
            qdarkstyle_lightss += "\nQPushButton{min-height:1.2em; min-width:3em}"
            self.styles["QDarkStyle-light"] = qdarkstyle_lightss

            # NOTE: following styles do not have supporting custom stylesheets
            # self.styles["fusion"] = ""
            # self.styles["windows"] = ""

        except ImportError:
            # if user has not install QDarkStyle, these stylesheets will not be available!
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

    def setStyle(self, style: str) -> None:
        """ NOTE: style is case sensitive! """
        if style in self.styles.keys():
            stylesheet = self.styles[style]
            # return self.styles[style]
            self.setStyleSheet(stylesheet)
            if style == "Chocolaf":
                self.setPalette(self.getPalette())
        elif style in QStyleFactory.keys():
            super(ChocolafApp, self).setStyle(style)
        else:
            availableStyles = self.availableStyles('all')
            msg = f"\"{style}\" is not recognized as a valid style!\nValid options are: [{availableStyles}]"
            raise ValueError(msg)
