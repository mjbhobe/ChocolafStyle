import sys
import numpy as np

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class Widget(QWidget):
    def __init__(self, parent: QWidget = None):
        super(Widget, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} Factorials")
        # create rest of layout here...
        self.setMinimumSize(640, 500)


def main():
    app: QApplication = QApplication(sys.argv)
    app.setStyle("Fusion")

    mainWin = QMainWindow()
    win: Widget = Widget()
    mainWin.setCentralWidget(win)
    mainWin.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
