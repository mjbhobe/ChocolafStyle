""" windarkPalette.py - Windows dark palette """
import pathlib
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *

from .palettes import WinDarkPalette
from .utilities import get_logger

_logger = get_logger(pathlib.Path(__file__).name)

WINDOWS_DARK_STYLE_SHEET = """
    QWidget:!active {
        background-color: rgb(32, 32, 32);    
        color: rgb(220, 220, 220);
    }
    QPushButton {
        min-height: 1.3em;
    }
    QMenuBar {
        background-color: rgb(25, 25, 25);
    }
    QMenu {
        background-color: rgb(25, 25, 25);
        selection-background-color: rgb(77, 77, 77);
    }
    QMenu::separator {
        height: 1px;
        background-color: rgb(77, 77, 77);
    }
    QToolBar {
        background-color: rgb(26, 32, 47);
    }
    QStatusBar {
        background-color: rgb(26, 32, 47);
    }
    QCheckBox:disabled {
        background-color: rgb(32, 32, 32);
        color: rgb(127, 127, 127);
    }
    QRadioButton:disabled {
        background-color: rgb(32, 32, 32);
        color: rgb(127, 127, 127);
    }
    QTreeView,
    QListView,
    QTableView,
    QColumnView {
        background-color: rgb(25, 25, 25);
        color: rgb(220, 220, 220); 
        gridline-color: rgb(102, 102, 102); 
        border-radius: 4px;
        line-height: 1.5em;
    }
    QTreeView::item:selected:!active,
    QListView::item:selected:!active,
    QTableView::item:selected:!active,
    QColumnView::item:selected:!active {
        color: rgb(220, 220, 220); 
        background-color: rgb(42, 42, 42); 
    }
    QLineEdit:disabled,
    QSpinBox:disabled,
    QDateTimeEdit:disabled,
    QTreeView:disabled,
    QListView:disabled,
    QTableView:disabled,
    QColumnView:disabled {
        background-color: rgb(42, 42, 42);
        color: rgb(127, 127, 127);
    }
"""


def setWindowsPaletteAndStyleSheet(app: QApplication):
    app.setStyle("Fusion")
    app.setFont(QApplication.font("QMenu"))
    palette = QPalette()
    # @see: https://doc.qt.io/qt-5/qpalette.html
    palette.setColor(
        QPalette.ColorGroup.Active, QPalette.ColorRole.Window,
        WinDarkPalette.Window_Color
    )  # general background color
    palette.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window,
        WinDarkPalette.Window_Color
    )  # general background color
    palette.setColor(
        QPalette.ColorGroup.Active,
        QPalette.ColorRole.WindowText,
        WinDarkPalette.WindowText_Color
    )  # general foreground color
    palette.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText,
        WinDarkPalette.Disabled_WindowText_Color
    )  # general foreground color
    palette.setColor(
        QPalette.ColorGroup.Active, QPalette.ColorRole.Base,
        WinDarkPalette.Base_Color
    )  # background for text entry widgets
    # background color for views with alternating colors
    palette.setColor(
        QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase,
        WinDarkPalette.AlternateBase_Color
    )
    palette.setColor(
        QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase,
        WinDarkPalette.ToolTipBase_Color
    )  # background for tooltips
    palette.setColor(
        QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText,
        WinDarkPalette.Placeholder_Color
    )
    palette.setColor(
        QPalette.ColorGroup.Active, QPalette.ColorRole.Text,
        WinDarkPalette.Text_Color
    )  # foreground color to use with Base
    palette.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text,
        WinDarkPalette.Disabled_Text_Color
    )
    palette.setColor(
        QPalette.ColorGroup.Active, QPalette.ColorRole.Dark,
        WinDarkPalette.Dark_Color
    )
    palette.setColor(
        QPalette.ColorGroup.Active, QPalette.ColorRole.Shadow,
        WinDarkPalette.Shadow_Color
    )
    palette.setColor(
        QPalette.ColorGroup.Active, QPalette.ColorRole.Button,
        WinDarkPalette.Button_Color
    )  # pushbutton colors
    palette.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button,
        WinDarkPalette.Button_Color
    )  # disabled pushbutton colors
    palette.setColor(
        QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText,
        WinDarkPalette.ButtonText_Color
    )  # pushbutton's text color
    palette.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText,
        WinDarkPalette.Disabled_ButtonText_Color
    )
    palette.setColor(
        QPalette.ColorGroup.Active, QPalette.ColorRole.Link,
        WinDarkPalette.Link_Color
    )
    palette.setColor(
        QPalette.ColorGroup.Active, QPalette.ColorRole.LinkVisited,
        WinDarkPalette.LinkVisited_Color
    )
    palette.setColor(
        QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight,
        WinDarkPalette.Highlight_Color
    )  # highlight color
    palette.setColor(
        QPalette.ColorGroup.Active, QPalette.ColorRole.HighlightedText,
        WinDarkPalette.HighlightedText_Color
    )
    palette.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light,
        WinDarkPalette.Disabled_Light_Color
    )

    app.setPalette(palette)
    app.setStyleSheet(WINDOWS_DARK_STYLE_SHEET)
