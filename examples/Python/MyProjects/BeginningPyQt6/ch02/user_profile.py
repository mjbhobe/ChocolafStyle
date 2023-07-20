""" labels.py - creating simple GUI using QLabels """
import sys
import os

from PyQt6.QtCore import PYQT_VERSION_STR
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QFont, QPixmap

AppDir = os.path.dirname(__file__)


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

    def setupMainWindow(self):
        self.createImageLabels()

        user_label = QLabel(self)
        user_label.setText("John Doe")
        user_label.setFont(QFont("Arial", 20))
        user_label.move(70, 140)

        bio_label = QLabel(self)
        bio_label.setText("Biography")
        bio_label.setFont(QFont("Arial", 16))
        bio_label.move(10, 170)

        about_label = QLabel(self)
        about_label.setText("Software developer with over 10 years " "experience creating awesome code")
        about_label.setWordWrap(True)
        about_label.move(10, 200)

        skills_label = QLabel(self)
        skills_label.setText("Skills")
        skills_label.setFont(QFont("Arial", 16))
        skills_label.move(10, 240)

        languages_label = QLabel(self)
        languages_label.setText("Python | Java | C++ | SQL | Tensorflow")
        languages_label.move(10, 265)

        experience_label = QLabel(self)
        experience_label.setText("Experience")
        experience_label.setFont(QFont("Arial", 16))
        experience_label.move(10, 290)

        developer_label = QLabel(self)
        developer_label.setText("Python Developer")
        developer_label.setFont(QFont("Arial", 10))
        developer_label.move(10, 315)

        dev_dates_label = QLabel(self)
        dev_dates_label.setText("Mar 2011 - Present")
        dev_dates_label.setFont(QFont("Arial", 8))
        dev_dates_label.move(10, 335)

        driver_label = QLabel(self)
        driver_label.setText("Pizza Delivery Driver")
        driver_label.setFont(QFont("Arial", 10))
        driver_label.move(10, 355)

        driver_dates_label = QLabel(self)
        driver_dates_label.setText("Aug 2015 - Dec 2017")
        driver_dates_label.setFont(QFont("Arial", 8))
        driver_dates_label.move(10, 375)


def main():
    app = QApplication(sys.argv)

    # create the main window
    win = MainWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
