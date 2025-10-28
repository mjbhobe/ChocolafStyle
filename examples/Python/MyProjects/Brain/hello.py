"""hello.py: basic PyQt6 application (Hello World)"""

import sys
import pathlib
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class MainWidget(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)
        self.label = None
        self.icon_path = str(pathlib.Path(__file__).parent / "Qt-logo.png")
        print(f"Icon: {self.icon_path}", flush=True)
        self.setupUi()

    def setupUi(self):
        self.label = QLabel(f"Welcome to PyQt {PYQT_VERSION_STR}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setWindowIcon(QIcon(self.icon_path))


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWidget()
    win.adjustSize()
    win.show()

    return app.exec()


if __name__ == "__main__":
    main()
