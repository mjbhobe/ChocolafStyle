# -*- coding: utf-8 -*-
"""
* displayImage.py - loads & displays image on a QLabel using
*   Qt functions (RGB color space) & OpenCV (BGR color space)
* @author (Chocolaf): Manish Bhobe
*
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!

"""
import sys
import cv2

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from chocolaf.palettes import ChocolafPalette
from chocolaf.utils.chocolafapp import ChocolafApp

import textEditor_rc

Window_Title = "PyQt Displaying Images with OpenCV"

# add some custom styling above & beyond stysheet set
style_sheet = """
    QLabel#ImageLabel {
        border: 2px dashed rgb(102, 102, 102);
    }
    QLabel {
        qproperty-alignment: AlignCenter;
    }
"""


class DisplayImageWindow(QMainWindow):
    def __init__(self, parent: QWidget = None):
        super(DisplayImageWindow, self).__init__(parent)
        self.initializeUi()
        # add custom styling to window
        self.setStyleSheet(style_sheet)

    def initializeUi(self):
        """ initialize all UI elements of window """
        self.setMinimumSize(850, 500)
        self.setWindowTitle(Window_Title)
        self.setupWindow()
        self.setupMenu()

    def setupWindow(self):
        """ setup the widgets in the main window """
        original_image_header = QLabel("Original Image")
        self.original_label = QLabel()
        self.original_label.setObjectName("ImageLabel")

        opencv_img_header = QLabel("OpenCV Image")
        self.opencv_label = QLabel()
        self.opencv_label.setObjectName("OpenCvImageLabel")

        # layout the widgets in 2 QVBoxLayout columns
        orig_layout = QVBoxLayout()
        orig_layout.addWidget(original_image_header)
        orig_layout.addWidget(self.original_label, 1)

        opencv_layout = QVBoxLayout()
        opencv_layout.addWidget(opencv_img_header)
        opencv_layout.addWidget(self.opencv_label, 1)

        main_layout = QHBoxLayout()
        main_layout.addLayout(orig_layout, Qt.AlignCenter)
        main_layout.addLayout(opencv_layout, Qt.AlignCenter)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def setupMenu(self):
        openAction = QAction(QIcon(":/file_open.png"), "&Open...", self)
        openAction.setShortcut(QKeySequence.Open)
        openAction.setStatusTip("Open an image file from disk")
        openAction.triggered.connect(self.openImage)

        exitAction = QAction(QIcon(":/on-off.png"), "E&xit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Quit the application")
        exitAction.triggered.connect(qApp.quit)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

    def openImage(self):
        picsLoc = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)
        print(f"{picsLoc[-1]}")
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", picsLoc[-1],
                                                    "Image files (*.png, *.tiff. *.jpg *.jpeg *.bmp)")
        if image_file:
            image = QImage()
            image.load(image_file)

            # show original
            self.original_label.setPixmap(QPixmap.fromImage(image).scaled(
                self.original_label.width(), self.original_label.height(),
                Qt.KeepAspectRatioByExpanding
            ))

            # display openCv image
            converted_image = self.convertCV2QImage(image_file)
            self.opencv_label.setPixmap(QPixmap.fromImage(converted_image).scaled(
                self.opencv_label.width(), self.opencv_label.height(),
                Qt.KeepAspectRatioByExpanding
            ))
            # and adjust size of main window to better accommodate images
            self.adjustSize()
            self.setWindowTitle(f"{Window_Title} - {image_file}")
        else:
            QMessageBox.information(self, "Error", "No image was loaded", QMessageBox.Ok)

    def convertCV2QImage(self, image_file):
        """ converts a OpenCV loaded image to QImage"""
        cv_image = cv2.imread(image_file)
        # un-comment the following line to convert image to RGB colorspace
        # cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        # get dimensions of image
        height, width, channels = cv_image.shape
        bytes_per_line = width * channels
        converted_QImage = QImage(cv_image, width, height, bytes_per_line,
                                  QImage.Format_RGB888)
        return converted_QImage


if __name__ == "__main__":
    app = ChocolafApp(sys.argv)
    app.setStyle("Chocolaf")

    win = DisplayImageWindow()
    win.show()

    sys.exit(app.exec())
