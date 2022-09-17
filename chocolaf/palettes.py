# -*- coding: utf-8 -*-
"""
* palettes.py - allows you earier access to certain key color components
*   of themes supported by Chocolaf
* @author: Manish Bhobe
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""

from PyQt5.QtGui import QColor, qRgb


class ChocolafPalette:
    # default background color for all widgets
    Window_Color = QColor(qRgb(42, 42, 42))
    # default foreground color for text
    WindowText_Color = QColor(qRgb(220, 220, 220))
    # disabled window text color
    Disabled_WindowText_Color = QColor(qRgb(127, 127, 127))
    # background for text entry widgets
    Base_Color = QColor(qRgb(52, 52, 52))
    # foreground color to use with Base
    Text_Color = QColor(qRgb(220, 220, 220))
    # disabled text foreground color
    Disabled_Text_Color = QColor(qRgb(127, 127, 127))
    # background color for views with alternating colors
    AlternateBase_Color = QColor(qRgb(62, 62, 62))
    # background color for tooltips
    ToolTipBase_Color = QColor(qRgb(224, 227, 176))
    # text color for tooltips
    ToolTipText_Color = QColor(qRgb(0, 0, 0))
    # pushbutton background color
    Button_Color = QColor(qRgb(62, 62, 62))
    # button text color
    ButtonText_Color = QColor(qRgb(220, 220, 220))
    # disabled pushbutton foreground color
    Disabled_ButtonText_Color = QColor(qRgb(127, 127, 127))
    # HTML link color
    Link_Color = QColor(qRgb(0, 0, 255))
    # visited link color
    LinkVisited_Color = QColor(qRgb(255, 0, 255))
    # background color of highlight (or selected) text or item
    Highlight_Color = QColor(qRgb(0, 114, 198))
    # foreground color of highlight (or selected) text or item
    HighlightedText_Color = QColor(qRgb(220, 220, 220))
    # faded text color (used for grid line color)
    Disabled_Light_Color = QColor(qRgb(102, 102, 102))
    # default border color
    Border_Color = QColor(qRgb(127, 127, 127))
    # disabled border color
    Disabled_Border_Color = QColor(qRgb(102, 102, 102))
