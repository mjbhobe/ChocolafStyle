""" labels.py - creating simple GUI using QLabels """
import sys
import os

from PyQt6.QtCore import PYQT_VERSION_STR
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QPixmap

AppDir = os.path.dirname(__file__)


class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super(MainWindow, self).__init__(parent)
        self.initializeUi()

    def initializeUi(self):
        self.setGeometry(100, 100, 250, 250)
        self.setWindowTitle(f"Welcome to PyQt {PYQT_VERSION_STR}")
        self.setupMainWindow()

    def setupMainWindow(self):
        hello_label = QLabel(self)
        hello_label.setText("Hello")
        hello_label.move(105, 15)

        image_path = os.path.join(AppDir, "images/world.png")
        if os.path.exists(image_path):
            world_label = QLabel(self)
            pixmap = QPixmap(image_path)
            world_label.setPixmap(pixmap)
            world_label.move(25, 40)
        else:
            raise FileNotFoundError(f"Unable to locate image {image_path}")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # create the main window
    win = MainWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
