# -*- coding: utf-8 -*-
"""
* imageProcessing.py - ilustrate some transformations & effects available
*   with OpenCV that can be applied to images.
* @author (Chocolaf): Manish Bhobe
*
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!

"""
import sys
import os
import cv2
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from chocolaf.palettes import ChocolafPalette
from chocolaf.utils.chocolafapp import ChocolafApp

import textEditor_rc

Window_Title = "PyQt Image Processing with OpenCV"

# add some custom styling above & beyond stysheet set
style_sheet = """ 
    QLabel#ImageLabel {
        border: 2px dashed rgb(102, 102, 102);
        qproperty-alignment: AlignCenter;
    }
"""


class ImageProcessingWindow(QMainWindow):
    def __init__(self, parent: QWidget = None):
        super(ImageProcessingWindow, self).__init__(parent)
        self.initializeUi()
        # add custom styling
        self.setStyleSheet(style_sheet)

    def initializeUi(self):
        """ initialize all UI elements of window """
        self.setMinimumSize(900, 600)
        self.setWindowTitle(Window_Title)
        self.contrastAdjusted = False
        self.brightnessAdjusted = False
        self.imageSmoothingChecked = False
        self.edgeDetectionChecked = False

        self.setupWindow()
        self.setupMenu()

    def setupWindow(self):
        """ setup the widgets in the main window """
        self.imageLabel = QLabel()
        self.imageLabel.setObjectName("ImageLabel")
        # self.imageLabel.setStyleSheet(style_sheet)

        # create the widgets in the image effects panel
        contrastLabel = QLabel("Contrast [Range: 0.0:4.0]")
        self.contrastSpinBox = QDoubleSpinBox()
        self.contrastSpinBox.setMinimumWidth(100)
        self.contrastSpinBox.setRange(0.0, 4.0)
        self.contrastSpinBox.setValue(1.0)
        self.contrastSpinBox.setSingleStep(0.10)
        self.contrastSpinBox.valueChanged.connect(self.adjustContrast)

        brightnessLabel = QLabel("Brightness [Range: -127:127]")
        self.brightnessSpinBox = QSpinBox()
        self.brightnessSpinBox.setMinimumWidth(100)
        self.brightnessSpinBox.setRange(-127, 127)
        self.brightnessSpinBox.setValue(1)
        self.brightnessSpinBox.setSingleStep(1)
        self.brightnessSpinBox.valueChanged.connect(self.adjustBrightness)

        smoothingLabel = QLabel("Image Smoothing Filters")
        self.filter2DCheckBox = QCheckBox("2D Convolution")
        self.filter2DCheckBox.stateChanged.connect(self.imageSmoothingFilter)

        edgesLabel = QLabel("Detect Edges")
        self.cannyCheckBox = QCheckBox("Canny Edge Detector")
        self.cannyCheckBox.stateChanged.connect(self.edgeDetection)

        self.applyButton = QPushButton("Apply Processes")
        self.applyButton.setEnabled(False)
        self.applyButton.clicked.connect(self.applyImageProcessing)

        self.resetButton = QPushButton("Reset Image Settings")
        self.resetButton.clicked.connect(self.resetImageAndSettings)

        # layout the widgets in 2 QVBoxLayout columns
        sidePanelVBox = QVBoxLayout()
        sidePanelVBox.setAlignment(Qt.AlignTop)
        sidePanelVBox.addWidget(contrastLabel)
        sidePanelVBox.addWidget(self.contrastSpinBox)
        sidePanelVBox.addWidget(brightnessLabel)
        sidePanelVBox.addWidget(self.brightnessSpinBox)
        sidePanelVBox.addSpacing(15)
        sidePanelVBox.addWidget(smoothingLabel)
        sidePanelVBox.addWidget(self.filter2DCheckBox)
        sidePanelVBox.addWidget(edgesLabel)
        sidePanelVBox.addWidget(self.cannyCheckBox)
        sidePanelVBox.addSpacing(15)
        sidePanelVBox.addWidget(self.applyButton)
        sidePanelVBox.addStretch(1)
        sidePanelVBox.addWidget(self.resetButton)

        sidePanelFrame = QFrame()
        sidePanelFrame.setMinimumWidth(200)
        sidePanelFrame.setFrameStyle(QFrame.WinPanel)
        sidePanelFrame.setLayout(sidePanelVBox)

        mainHBox = QHBoxLayout()
        mainHBox.addWidget(self.imageLabel, 1)
        mainHBox.addWidget(sidePanelFrame)

        container = QWidget()
        container.setLayout(mainHBox)
        self.setCentralWidget(container)

    def setupMenu(self):
        openAction = QAction(QIcon(":/file_open.png"), "&Open...", self)
        openAction.setShortcut(QKeySequence.Open)
        openAction.setStatusTip("Open an image file from disk")
        openAction.triggered.connect(self.openImage)

        saveAction = QAction(QIcon(":/file_save.png"), "&Save...", self)
        saveAction.setShortcut(QKeySequence.Save)
        saveAction.setStatusTip("Save modified image to disk")
        saveAction.triggered.connect(self.saveImage)

        exitAction = QAction(QIcon(":/on-off.png"), "E&xit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Quit the application")
        exitAction.triggered.connect(qApp.quit)

        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

    def adjustContrast(self):
        if self.imageLabel.pixmap() != None:
            self.contrastAdjusted = True

    def adjustBrightness(self):
        if self.imageLabel.pixmap() != None:
            self.brightnessAdjusted = True

    def imageSmoothingFilter(self, state):
        if state == Qt.Checked and self.imageLabel.pixmap() != None:
            self.imageSmoothingChecked = True
        elif state != Qt.Checked and self.imageLabel.pixmap() != None:
            self.imageSmoothingChecked = False

    def edgeDetection(self, state):
        if state == Qt.Checked and self.imageLabel.pixmap() != None:
            self.edgeDetectionChecked = True
        elif state != Qt.Checked and self.imageLabel.pixmap() != None:
            self.edgeDetectionChecked = False

    def applyImageProcessing(self):
        """For the boolean variables related to the image processing
        techniques, if True, apply the corresponding process to the image
        and display the changes in the QLabel, image_label."""
        if self.contrastAdjusted == True or self.brightnessAdjusted == True:
            contrast = self.contrastSpinBox.value()
            brightness = self.brightnessSpinBox.value()
            self.cv_image = cv2.convertScaleAbs(self.cv_image, self.processed_cv_image,
                                                contrast, brightness)
        if self.imageSmoothingChecked == True:
            kernel = np.ones((5, 5), np.float32) / 25
            self.cv_image = cv2.filter2D(self.cv_image, -1, kernel)
        if self.edgeDetectionChecked == True:
            self.cv_image = cv2.Canny(self.cv_image, 100, 200)
        self.convertCV2QImage(self.cv_image)
        self.imageLabel.repaint()  # Repaint the updated image on the label

    def resetImageAndSettings(self):
        """Reset the displayed image and widgets used for image
        processing."""
        answer = QMessageBox.information(self, "Reset Image",
                                         "Are you sure you want to reset the image settings?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if answer == QMessageBox.No:
            pass
        elif answer == QMessageBox.Yes and self.imageLabel.pixmap() != None:
            self.resetWidgetValues()
            self.cv_image = self.copy_cv_image
            self.convertCV2QImage(self.copy_cv_image)

    def resetWidgetValues(self):
        self.contrastSpinBox.setValue(1.0)
        self.brightnessSpinBox.setValue(0)
        self.filter2DCheckBox.setChecked(False)
        self.cannyCheckBox.setChecked(False)

    def openImage(self):
        picsLoc = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", picsLoc[-1],
                                                    "Image files (*.png, *.tiff. *.jpg *.jpeg *.bmp)")
        if image_file:
            self.resetWidgetValues()
            self.applyButton.setEnabled(True)

            self.cv_image = cv2.imread(image_file)
            self.copy_cv_image = self.cv_image
            self.processed_cv_image = np.zeros(self.cv_image.shape, self.cv_image.dtype)
            self.convertCV2QImage(self.cv_image)
        else:
            QMessageBox.information(self, "Error", "No image was loaded", QMessageBox.Ok)

    def saveImage(self):
        picsLoc = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)
        image_file, _ = QFileDialog.getSaveFileName(self, "Open Image", picsLoc[-1],
                                                    "Image files (*.png, *.tiff. *.jpg *.jpeg *.bmp)")
        if image_file and self.imageLabel.pixmap() != None:
            cv2.imwrite(image_file, self.cv_image)
        else:
            QMessageBox.information(self, "Error", "Unable to save image", QMessageBox.Ok)

    def convertCV2QImage(self, image_file):
        """ converts a OpenCV loaded image to QImage"""
        cv_image = cv2.cvtColor(image_file, cv2.COLOR_BGR2RGB)
        # get dimensions of image
        height, width, channels = cv_image.shape
        bytes_per_line = width * channels
        converted_QImage = QImage(cv_image, width, height, bytes_per_line,
                                  QImage.Format_RGB888)
        self.imageLabel.setPixmap(QPixmap.fromImage(converted_QImage.scaled(
            self.imageLabel.width(), self.imageLabel.height(),
            Qt.KeepAspectRatio
        )))
        return converted_QImage


if __name__ == "__main__":
    app = ChocolafApp(sys.argv)
    app.setStyle("Chocolaf")

    win = ImageProcessingWindow()
    win.imageLabel.setStyleSheet(style_sheet)
    win.show()

    sys.exit(app.exec())
