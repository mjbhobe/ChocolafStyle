""" checkboxes.py - create the basic PyQt6 application """
import sys

from PyQt6.QtCore import PYQT_VERSION_STR, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QCheckBox

import chocolaf

STYLE_SHEET = """
    QWidget {
       background-color: rgb(47, 47, 47);
        border: 0px solid rgb(127, 127, 127);
        padding: 0px;
        color: rgb(220, 220, 220);
        selection-background-color: rgb(0, 114, 198);
        selection-color: rgb(220, 220, 220);
    }

    QWidget:disabled {
        background-color: rgb(47, 47, 47);
        color: rgb(127, 127, 127);
        selection-background-color: rgb(43, 87, 154);
        selection-color: rgb(127, 127, 127);
    }

    QWidget::item:selected {
        background-color: rgb(0, 114, 198);
    }

    QWidget::item:hover: !selected {
        background: rgb(83, 88, 90);
        color: rgb(220, 220, 220);
    }    

    QLabel {
        background-color: rgb(47, 47, 47);
        color: rgb(220, 220, 220);
        border: none;
        padding: 2px;
        margin: 0px;
    }

    QLabel:disabled {
        background-color: rgb(47, 47, 47);
        border: none;
        color: rgb(127, 127, 127);
    }

    QCheckBox {
        background-color: rgb(27, 27, 27);
        color: rgb(220, 220, 220);
        spacing: 4px;
        padding-top: 4px;
        padding-bottom: 4px;
        height: 24px;
    }

    QCheckBox:focus {
        border: 1px solid rgb(220, 220, 220);
    }

    QCheckBox QWidget:disabled {
        background-color: rgb(37, 37, 37);
        color: rgb(127, 127, 127);
    }   
    
    QCheckBox::indicator {
      margin-left: 1px;
      height: 24px;
      width: 24px;
    } 
"""


# label_style = """
# QLabel {
#     background-color: rgb(47, 47, 47);
#     color: rgb(220, 220, 220);
#     border: none;
#     padding: 2px;
#     margin: 0px;
# }
#
# QLabel:disabled {
#     background-color: rgb(47, 47, 47);
#     border: none;
#     color: rgb(127, 127, 127);
# }
# """
#
# checkbox_style = """
# QCheckBox {
#     background-color: rgb(47, 47, 47);
#     color: rgb(220, 220, 220);
#     spacing: 4px;
#     border: 1px solid rgb(220, 220, 220);
#     outline: none;
#     padding-top: 4px;
#     padding-bottom: 4px;
# }
#
# QCheckBox:focus {
#     border: none;
# }
#
# QCheckBox QWidget:disabled {
#     background-color: rgb(47, 47, 47);
#     color: rgb(127, 127, 127);
# }
#
#
#
# """


class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super(MainWindow, self).__init__(parent)
        self.initializeUi()

    def initializeUi(self):
        self.setGeometry(200, 100, 250, 175)
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} checkboxes")
        self.setupMainWindow()

    def setupMainWindow(self):
        header_label = QLabel("Which shifts can you work?\n(Please check all that apply)", self)
        header_label.setWordWrap(True)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.move(10, 10)

        # Set up the checkboxes
        morning_cb = QCheckBox("Morning [8 AM-2 PM]", self)
        morning_cb.move(40, 60)
        morning_cb.toggled.connect(self.printSelected)
        morning_cb.toggle()  # Uncomment to start checked
        after_cb = QCheckBox("Afternoon [1 PM-8 PM]", self)
        after_cb.move(40, 90)
        after_cb.toggled.connect(self.printSelected)
        night_cb = QCheckBox("Night [7 PM-3 AM]", self)
        night_cb.move(40, 120)
        night_cb.toggled.connect(self.printSelected)

    def printSelected(self, checked):
        """print the text that teh sender is sending"""
        sender = self.sender()
        if checked:
            print(f"{sender.text()} selected")
        else:
            print(f"{sender.text()} de-selected")


def main():
    # chocolaf.enable_hi_dpi()
    # app = chocolaf.ChocolafApp(sys.argv)
    # app.setStyle("Chocolaf")
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE_SHEET)

    # create the main window
    win = MainWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
