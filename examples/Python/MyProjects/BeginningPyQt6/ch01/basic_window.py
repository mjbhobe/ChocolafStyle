""" basic_window.py - create the basic PyQt6 application """
import sys

from PyQt6.QtCore import PYQT_VERSION_STR, Qt
from PyQt6.QtWidgets import QApplication, QWidget


class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super(MainWindow, self).__init__(parent)
        self.initializeUi()

    def initializeUi(self):
        self.setGeometry(200, 100, 400, 300)
        self.setWindowTitle(f"Welcome to PyQt {PYQT_VERSION_STR}")
        self.setupMainWindow()

    def setupMainWindow(self):
        """ setup widgets & connect signals/slots """
        pass


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # create the main window
    win = MainWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
