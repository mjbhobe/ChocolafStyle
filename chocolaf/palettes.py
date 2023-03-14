# -*- coding: utf-8 -*-
"""
* palettes.py - allows you earier access to certain key color components
*   of themes supported by Chocolaf
* @author: Manish Bhobe
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""

# from PyQt5.QtGui import QColor, qRgb
from qtpy.QtGui import QColor, qRgb
import qtawesome as qta


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
    # clostBtn text color
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


class WinDarkPalette:
    # default background color for all widgets
    Window_Color = QColor(qRgb(32, 32, 32))
    # default foreground color for text
    WindowText_Color = QColor(qRgb(220, 220, 220))
    # disabled window text color
    Disabled_WindowText_Color = QColor(qRgb(127, 127, 127))
    # background for text entry widgets
    Base_Color = QColor(qRgb(25, 25, 25))
    # background color for views with alternating colors
    AlternateBase_Color = QColor(qRgb(66, 67, 67))
    # background color for tooltips
    ToolTipBase_Color = QColor(qRgb(224, 227, 176))
    # text color for tooltips
    ToolTipText_Color = QColor(qRgb(0, 0, 0))
    # foreground color to use for placeholder text
    Placeholder_Color = QColor(qRgb(127, 127, 127))
    # foreground color to use with Base
    Text_Color = QColor(qRgb(220, 220, 220))
    # disabled text foreground colo7
    Disabled_Text_Color = QColor(qRgb(127, 127, 127))
    # darker than button color
    Dark_Color = QColor(qRgb(35, 35, 35))
    # shadow color
    Shadow_Color = QColor(qRgb(20, 20, 20))
    # pushbutton background color
    Button_Color = QColor(qRgb(45, 45, 45))
    # clostBtn text color
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


class ChocolafIcons:
    # file menu standard SVG icons from Material theme
    File_New_Icon = qta.icon("mdi6.file-document-outline")
    File_Open_Icon = qta.icon("mdi6.folder-open")
    File_Save_Icon = qta.icon("mdi6.content-save-outline")
    File_SaveAs_Icon = qta.icon("mdi6.content-save-edit-outline")
    File_SaveAll_Icon = qta.icon("mdi6.content-save-all-outline")
    File_Print = qta.icon("mdi6.printer")

    # edit menu standard SVG icons from Material theme
    Edit_Undo_Icon = qta.icon("mdi6.undo")
    Edit_Redo_Icon = qta.icon("mdi6.redo")
    Edit_Cut_Icon = qta.icon("mdi6.content-cut")
    Edit_Copy_Icon = qta.icon("mdi6.content-copy")
    Edit_Paste_Icon = qta.icon("mdi6.content-paste")
    Edit_Delete_Icon = qta.icon("mdi6.trash-can-outline")
    Edit_SelectAll_Icon = qta.icon("mdi6.select-all")

    # alignment
    Align_Left_Icon = qta.icon("mdi6.align-horizontal-left")
    Align_Right_Icon = qta.icon("mdi6.align-horizontal-right")
    Align_Top_Icon = qta.icon("mdi6.align-vertical-right")
    Align_Bottom_Icon = qta.icon("mdi6.align-vertical-bottom")
    Align_HCenter_Icon = qta.icon("mdi6.align-horizontal-center")
    Align_VCenter_Icon = qta.icon("mdi6.align-vertical-center")
    Align_HDistribute_Icon = qta.icon("mdi6.align-horizontal-distribute")
    Align_VDistribute_Icon = qta.icon("mdi6.align-vertical-distribute")
    Format_ParaAlignLeft_Icon = qta.icon("mdi6.format-align-left")
    Format_ParaAlignCenter_Icon = qta.icon("mdi6.format-align-center")
    Format_ParaAlignRight_Icon = qta.icon("mdi6.format-align-right")
    Format_ParaAlignJustify_Icon = qta.icon("mdi6.format-align-justify")

    # search
    Search_Find_Icon = qta.icon("mdi6.magnify")
    Search_FindFile_Icon = qta.icon("mdi6.find-file-outline")
    Search_Replace_Icon = qta.icon("mdi6.find-replace")

    # zoom
    Zoom_In_Icon = qta.icon("mdi6.magnify-plus-outline")
    Zoom_Out_Icon = qta.icon("mdi6.magnify-minus-outline")
    Zoom_FitWindow_Icon = qta.icon("mdi6.fit-to-screen-outline")
    Zoom_ExpandAllLeft_Icon = qta.icon("mdi6.arrow-expand-left")
    Zoom_ExpandAllUp_Icon = qta.icon("mdi6.arrow-expand-up")
    Zoom_ExpandAllRight_Icon = qta.icon("mdi6.arrow-expand-right")
    Zoom_ExpandAllDown_Icon = qta.icon("mdi6.arrow-expand-down")
    Zoom_ExpandAll_Icon = qta.icon("mdi6.arrow-expand-all")
    Zoom_CollapseAll_Icon = qta.icon("mdi6.arrow-collapse-all")

    # navigation
    Navig_ArrowLeft_Icon = qta.icon("mdi6.arrow-left")
    Navig_ArrowUp_Icon = qta.icon("mdi6.arrow-up")
    Navig_ArrowRight_Icon = qta.icon("mdi6.arrow-right")
    Navig_ArrowDown_Icon = qta.icon("mdi6.arrow-down")

    Navig_ChevronLeft_Icon = qta.icon("mdi6.chevron-left")
    Navig_ChevronDoubleLeft_Icon = qta.icon("mdi6.chevron-double-left")
    Navig_ChevronUp_Icon = qta.icon("mdi6.chevron-up")
    Navig_ChevronDoubleUp_Icon = qta.icon("mdi6.chevron-double-up")
    Navig_ChevronRight_Icon = qta.icon("mdi6.chevron-right")
    Navig_ChevronDoubleRight_Icon = qta.icon("mdi6.chevron-double-right")
    Navig_ChevronDown_Icon = qta.icon("mdi6.chevron-down")
    Navig_ChevronDoubleDown_Icon = qta.icon("mdi6.chevron-double-down")
    Navig_ChevronPageFirst_Icon = qta.icon("mdi6.page-first")
    Navig_ChevronPageLast_Icon = qta.icon("mdi6.page-last")

    # rotation
    Rotate_Left_Icon = qta.icon("mdi6.rotate-left")
    Rotate_Right_Icon = qta.icon("mdi6.rotate-right")
    Flip_Left_Icon = qta.icon("mdi6.rotate-left-variant")
    Flip_Right_Icon = qta.icon("mdi6.rotate-right-variant")
