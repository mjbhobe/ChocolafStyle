""" labels.py - creating simple GUI using QLabels """
import sys
import os

from PyQt6.QtCore import PYQT_VERSION_STR
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QPixmap

# You can run this Python script from anywhere. As it uses images from
# the images sub-folder, it's important to determine the dirname of this
# script, so we can load images from it's subfolder
AppDir = os.path.dirname(__file__)


class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super(MainWindow, self).__init__(parent)
        self.initializeUi()

    def initializeUi(self):
        """create the main window & set attributes"""
        self.setGeometry(100, 100, 250, 250)
        self.setWindowTitle(f"Hello PyQt{PYQT_VERSION_STR}")
        self.setupMainWindow()

    def setupMainWindow(self):
        """setup child controls in main window, connect signals/slots"""
        hello_label = QLabel(self)
        hello_label.setText(f"PtQt {PYQT_VERSION_STR} labels demo (no layout)")
        hello_label.move(25, 15)

        # load images from sub-folder of AppDir
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
