import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

# using qdarkstyle (@see: https://github.com/ColinDuquesnoy/QDarkStyleSheet)
import qdarkstyle

# to detect dark themes (@see: https://pypi.org/project/darkdetect/)
import darkdetect


class Hello(QWidget):
    def __init__(self):
        super().__init__()
        self.initGui()

    def initGui(self):
        self.setWindowTitle(f"Hello PyQt {PYQT_VERSION_STR} World")
        hello = QLabel("Welcome to PyQt programming. Enjoy the ride!")
        quitBtn = QPushButton("Quit!")
        quitBtn.setMinimumWidth(100)
        quitBtn.setToolTip("Quit application")
        layout1 = QHBoxLayout()
        layout1.addWidget(hello)
        layout1.addWidget(quitBtn)
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(layout1)
        self.setLayout(mainLayout)

        # signals & slots
        quitBtn.clicked.connect(QApplication.instance().quit)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    if darkdetect.isDark():
        # apply dark stylesheet
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt5"))

    w = Hello()
    # w.setGeometry(100, 100, 640, 480)
    w.show()

    return app.exec()


if __name__ == "__main__":
    main()
