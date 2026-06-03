""" labels.py - creating simple GUI using QLabels """
import sys
import os
from typing import Literal

from PyQt6.QtCore import PYQT_VERSION_STR
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QFont, QPixmap

# You can run this Python script from anywhere. As it uses images from
# the images sub-folder, it's important to determine the dirname of this
# script, so we can load images from it's subfolder
AppDir = os.path.dirname(__file__)

# Here is how you specify a font-chain to use, in case your favourite font
# is not available on the OS - PyQt works on several OS with no code change
font_chain = ["Arial", "Helvetica", "Noto Sans", "Liberation Sans", "Sans-Serif"]
base_gui_font: QFont = QFont()
base_gui_font.setFamilies(font_chain)

# Define the exact allowable string choices
FontStyle = Literal["plain", "bold", "italic", "bold & italic"]


class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super(MainWindow, self).__init__(parent)
        self.initializeUi()

    def initializeUi(self):
        self.setGeometry(100, 100, 250, 400)
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} - User Profile")
        self.setupMainWindow()
        self.setFixedSize(self.size())

    def createImageLabels(self):
        images = [os.path.join(AppDir, img) for img in ["images/skyblue.png", "images/profile_image.png"]]
        for image_path in images:
            if os.path.exists(image_path):
                label = QLabel(self)
                pixmap = QPixmap(image_path)
                label.setPixmap(pixmap)
            if image_path.endswith("profile_image.png"):
                label.move(80, 20)

    def customBaseFont(self, pointSize: int, style: FontStyle = 'plain') -> QFont:
        """create a custom point font from base gui_font"""
        cust_font = QFont(base_gui_font)
        cust_font.setPointSize(pointSize)

        # customize styles, if specified
        if style == "bold":
            cust_font.setBold(True)
        elif style == "italic":
            cust_font.setItalic(True)
        elif style == "bold & italic":
            cust_font.setBold(True)
            cust_font.setItalic(True)

        return cust_font

    def setupMainWindow(self):
        self.createImageLabels()

        user_label = QLabel(self)
        user_label.setText("John Doe")
        #user_label.setFont(QFont("Arial", 20))
        user_label.setFont(self.customBaseFont(20))
        user_label.move(70, 140)

        bio_label = QLabel(self)
        bio_label.setText("Biography")
        # bio_label.setFont(QFont("Arial", 16))
        bio_label.setFont(self.customBaseFont(14))
        bio_label.move(10, 170)

        about_label = QLabel(self)
        about_label.setText("Software dev with 10+ years of experience creating awesome code")
        about_label.setWordWrap(True)
        about_label.move(10, 200)

        skills_label = QLabel(self)
        skills_label.setText("Skills")
        # skills_label.setFont(QFont("Arial", 16))
        skills_label.setFont(self.customBaseFont(14))
        skills_label.move(10, 240)

        languages_label = QLabel(self)
        languages_label.setText("Python | Java | C++ | SQL | PyTorch")
        languages_label.setFont(self.customBaseFont(10))
        languages_label.move(10, 265)

        experience_label = QLabel(self)
        experience_label.setText("Experience")
        # experience_label.setFont(QFont("Arial", 16))
        experience_label.setFont(self.customBaseFont(14))
        experience_label.move(10, 290)

        developer_label = QLabel(self)
        developer_label.setText("Python Developer")
        # developer_label.setFont(QFont("Arial", 10))
        developer_label.setFont(self.customBaseFont(10, "italic"))
        developer_label.move(10, 315)

        dev_dates_label = QLabel(self)
        dev_dates_label.setText("Mar 2011 - Present")
        # dev_dates_label.setFont(QFont("Arial", 8))
        dev_dates_label.setFont(self.customBaseFont(8))
        dev_dates_label.move(10, 335)

        driver_label = QLabel(self)
        driver_label.setText("Pizza Delivery Driver")
        #driver_label.setFont(QFont("Arial", 10))
        driver_label.setFont(self.customBaseFont(10, "italic"))
        driver_label.move(10, 355)

        driver_dates_label = QLabel(self)
        driver_dates_label.setText("Aug 2015 - Dec 2017")
        #driver_dates_label.setFont(QFont("Arial", 8))
        driver_dates_label.setFont(self.customBaseFont(8))
        driver_dates_label.move(10, 375)


def main():
    app = QApplication(sys.argv)

    # create the main window
    win = MainWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
