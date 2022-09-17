#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
* ImageViewer.py: Image viewer application with PyQt and OpenCV
* @author (Chocolaf): Manish Bhobe
*
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import os
import sys
import cv2
from argparse import ArgumentParser

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from chocolaf.utils.chocolafapp import ChocolafApp
from ImageSpinner import ImageSpinner
import ImageViewer_rc


class ImageViewer(QMainWindow):
    """ main display window """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.imageLoaded = False
        self.imageLabel = QLabel("")
        self.imageCountLabel = QLabel("")
        self.scaleFactorLabel = QLabel("")
        self.imageInfoLabel = QLabel("")
        self.scrollArea = QScrollArea()
        self.cv2image = None        # OpenCV Mat
        self.image = None           # QImage
        self.scaleFactor = 1.0
        self.firstDialog = True
        self.imageSpinner = None
        self.setupUi()

    def setupUi(self):
        """ helper function to layout UI elements """
        self.imageLabel.setBackgroundRole(QPalette.Base)
        # don't automatically resize label
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # scale label to fit image
        self.imageLabel.setScaledContents(True)

        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)
        self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createMenu()
        self.createToolbar()
        # and status bar
        self.statusBar().showMessage(
            f"Image Viewer: developed with PyQt {PYQT_VERSION_STR} by Manish Bhobe")
        self.setupStatusBar()

        self.resize(QGuiApplication.primaryScreen().availableSize() * (4 / 5))
        self.setWindowIcon(QIcon(":/app_icon.png"))

    def createActions(self):
        # open image
        self.openAction = QAction("&Open...", self)
        self.openAction.setShortcut(QKeySequence.New)
        self.openAction.setIcon(QIcon(":/open.png"))
        self.openAction.setStatusTip("Open a new image file to view")
        self.openAction.triggered.connect(self.open)

        # print image
        self.printAction = QAction("&Print...", self)
        self.printAction.setShortcut(QKeySequence.Print)
        self.printAction.setIcon(QIcon(":/print.png"))
        self.printAction.setStatusTip("Print the current image")
        self.printAction.triggered.connect(self.print)
        self.printAction.setEnabled(False)

        # exit
        self.exitAction = QAction("E&xit", self)
        self.exitAction.setShortcut(QKeySequence("Ctrl+Q"))
        self.exitAction.setStatusTip("Exit the application")
        self.exitAction.triggered.connect(QApplication.instance().quit)

        # View category...
        self.zoomInAction = QAction("Zoom &in (25%)", self)
        self.zoomInAction.setShortcut(QKeySequence("Ctrl++"))
        self.zoomInAction.setIcon(QIcon(":/zoom_in.png"))
        self.zoomInAction.setStatusTip("Zoom into the image by 25%")
        self.zoomInAction.triggered.connect(self.zoomIn)
        self.zoomInAction.setEnabled(False)

        self.zoomOutAction = QAction("Zoom &out (25%)", self)
        self.zoomOutAction.setShortcut(QKeySequence("Ctrl+-"))
        self.zoomOutAction.setIcon(QIcon(":/zoom_out.png"))
        self.zoomOutAction.setStatusTip("Zoom out of the image by 25%")
        self.zoomOutAction.triggered.connect(self.zoomOut)
        self.zoomOutAction.setEnabled(False)

        self.zoomNormalAction = QAction("&Normal size", self)
        self.zoomNormalAction.setShortcut(QKeySequence("Ctrl+0"))
        self.zoomNormalAction.setStatusTip("Zoom to normal size")
        self.zoomNormalAction.triggered.connect(self.zoomNormal)
        self.zoomNormalAction.setEnabled(False)

        self.rotateLeftAction = QAction("Rotate &left", self)
        self.rotateLeftAction.setShortcut(QKeySequence("Ctrl+<"))
        self.rotateLeftAction.setIcon(QIcon(":/rotate_left.png"))
        self.rotateLeftAction.setStatusTip("Rotate image left by 90 degrees")
        self.rotateLeftAction.triggered.connect(self.rotateLeft)
        self.rotateLeftAction.setEnabled(False)

        self.rotateRightAction = QAction("Rotate &right", self)
        self.rotateRightAction.setShortcut(QKeySequence("Ctrl+>"))
        self.rotateRightAction.setIcon(QIcon(":/rotate_right.png"))
        self.rotateRightAction.setStatusTip("Rotate image right by 90 degrees")
        self.rotateRightAction.triggered.connect(self.rotateRight)
        self.rotateRightAction.setEnabled(False)

        self.fitToWindowAction = QAction("Fit to &window", self)
        self.fitToWindowAction.setShortcut(QKeySequence("Ctrl+1"))
        self.fitToWindowAction.setIcon(QIcon(":/zoom_fit.png"))
        self.fitToWindowAction.setStatusTip("Fit image to size of window")
        self.fitToWindowAction.triggered.connect(self.fitToWindow)
        self.fitToWindowAction.setEnabled(False)
        self.fitToWindowAction.setCheckable(True)

        self.prevImageAction = QAction("&Previous Image", self)
        self.prevImageAction.setShortcut(QKeySequence.MoveToPreviousChar)
        self.prevImageAction.setIcon(QIcon(":/go_prev.png"))
        self.prevImageAction.setStatusTip("View previous image in folder")
        self.prevImageAction.triggered.connect(self.prevImage)
        self.prevImageAction.setEnabled(False)

        self.nextImageAction = QAction("&Next Image", self)
        self.nextImageAction.setShortcut(QKeySequence.MoveToNextChar)
        self.nextImageAction.setIcon(QIcon(":/go_next.png"))
        self.nextImageAction.setStatusTip("View next image in folder")
        self.nextImageAction.triggered.connect(self.nextImage)
        self.nextImageAction.setEnabled(False)

        # Help category
        self.aboutAction = QAction("&About...", self)
        self.aboutAction.setStatusTip("Display about application information")
        self.aboutAction.triggered.connect(self.about)

        self.aboutQtAction = QAction("About &Qt...", self)
        self.aboutQtAction.setStatusTip(
            "Display information about Qt library being used")
        self.aboutQtAction.triggered.connect(QApplication.instance().aboutQt)

    def createMenu(self):
        # file menu
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.printAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

        # view menu
        viewMenu = self.menuBar().addMenu("View")
        viewMenu.addAction(self.zoomInAction)
        viewMenu.addAction(self.zoomOutAction)
        viewMenu.addAction(self.zoomNormalAction)
        viewMenu.addAction(self.fitToWindowAction)
        viewMenu.addSeparator()
        viewMenu.addAction(self.rotateLeftAction)
        viewMenu.addAction(self.rotateRightAction)
        viewMenu.addSeparator()
        viewMenu.addAction(self.prevImageAction)
        viewMenu.addAction(self.nextImageAction)

        # help menu
        helpMenu = self.menuBar().addMenu("Help")
        helpMenu.addAction(self.aboutAction)
        helpMenu.addAction(self.aboutQtAction)

    def createToolbar(self):
        toolBar = self.addToolBar("Main")
        toolBar.addAction(self.openAction)
        toolBar.addAction(self.printAction)
        toolBar.addSeparator()
        toolBar.addAction(self.zoomInAction)
        toolBar.addAction(self.zoomOutAction)
        toolBar.addAction(self.fitToWindowAction)
        toolBar.addAction(self.rotateLeftAction)
        toolBar.addAction(self.rotateRightAction)
        toolBar.addSeparator()
        toolBar.addAction(self.prevImageAction)
        toolBar.addAction(self.nextImageAction)

    def updateActions(self):
        self.fitToWindowAction.setEnabled(not (self.image is None))
        self.zoomInAction.setEnabled(not self.fitToWindowAction.isChecked())
        self.zoomOutAction.setEnabled(not self.fitToWindowAction.isChecked())
        self.zoomNormalAction.setEnabled(not self.fitToWindowAction.isChecked())
        self.rotateLeftAction.setEnabled(not (self.image is None))
        self.rotateRightAction.setEnabled(not (self.image is None))
        self.prevImageAction.setEnabled(not (self.image is None))
        self.nextImageAction.setEnabled(not (self.image is None))

    def setupStatusBar(self):
        self.statusBar().setStyleSheet("QStatusBar::item {border: none;}")
        self.statusBar().addPermanentWidget(self.imageInfoLabel)
        self.statusBar().addPermanentWidget(self.imageCountLabel)
        self.statusBar().addPermanentWidget(self.scaleFactorLabel)

    def updateStatusBar(self):
        """ update the various permanent widgets on the status bar """
        if self.imageSpinner is not None:
            imageInfoText = f"{self.image.width():4d} x {self.image.height():4d} {'grayscale' if self.image.isGrayscale() else 'color'}"
            self.imageInfoLabel.setText(imageInfoText)
            selImageText = f"{self.imageSpinner.currIndex+1:3d} of {self.imageSpinner.size():3d} images"
            self.imageCountLabel.setText(selImageText)
            scaleFactorText = "Zoom: Fit" if self.fitToWindowAction.isChecked() \
                else f"Zoom: {int(self.scaleFactor * 100)} %"
            self.scaleFactorLabel.setText(scaleFactorText)

    def openCV2QImage(self, cv2image):
        """ convert an OpenCV2 image read using cv2.imread to QImage """
        height, width, channels = cv2image.shape
        bytes_per_line = width * channels
        qimage = QImage(cv2image, width, height, bytes_per_line, QImage.Format_RGB888)
        return qimage

    def displayImageInfo(self):
        if self.image.isNull():
            return
        print(f"Image info -> width: {self.image.width()} - height: {self.image.height()} " +
              f"- bits/pixel: {self.image.depth()} - color: {not self.image.isGrayscale()}")

    def scaleImage(self, factor=-1):
        """scale image to a certain scaling factor. Default value of -1 is 
           only used to scale a newly loaded image to same scale factor as prev image
        """
        if factor != -1:
            self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())
        self.adjustScrollbar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollbar(self.scrollArea.verticalScrollBar(), factor)
        self.zoomInAction.setEnabled(self.scaleFactor < 5.0)
        self.zoomOutAction.setEnabled(self.scaleFactor > 0.10)
        #print(f"Scalefactor = {self.scaleFactor}")

    def adjustScrollbar(self, scrollBar: QScrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value() +
                               ((factor - 1) * scrollBar.pageStep() / 2)))

    def initOpenDialog(self, dialog: QFileDialog, acceptMode: QFileDialog.AcceptMode):
        picLocations = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)
        # print(f"Standard pic locations: {picLocations}")
        dialog.setDirectory(QDir.currentPath if len(picLocations) == 0 else picLocations[-1])
        supportedMimeTypes = (QImageReader.supportedMimeTypes() if acceptMode == QFileDialog.AcceptMode.AcceptOpen
                              else QImageWriter.supportedMimeTypes())
        mimeTypeFilters = [str(mimeTypeName, 'utf-8') for mimeTypeName in supportedMimeTypes]
        mimeTypeFilters = sorted(mimeTypeFilters)
        dialog.setMimeTypeFilters(mimeTypeFilters)
        dialog.selectMimeTypeFilter("image/jpeg")
        dialog.setAcceptMode(acceptMode)
        if (acceptMode == QFileDialog.AcceptMode.AcceptSave):
            dialog.setDefaultSuffix("jpg")

    def loadImage(self, imagePath):
        assert os.path.exists(imagePath), f"FATAL: could not load file {imagePath}"
        # reader = QImageReader(imagePath)
        # reader.setAutoTransform(True)
        # self.image = reader.read()
        # if self.image is None:
        #     QMessageBox.error(self, "ImageViewer", f"Could not load {imagePath}")
        #     return False

        self.cv2image = cv2.imread(imagePath)
        if self.cv2image.size == 0:
            QMessageBox.error(self, "ImageEditor", f"Could not load {imagePath}")
            return False
        else:
            self.cv2image = cv2.cvtColor(self.cv2image, cv2.COLOR_BGR2RGB)

        self.image = self.openCV2QImage(self.cv2image)

        # self.scaleFactor = 1.0
        self.scrollArea.setVisible(True)

        # self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
        # self.imageLabel.adjustSize()
        # # self.fitToWindow()
        # self.scaleImage()
        self.showImage(self.image)

        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} Image Viewer: {imagePath}")

        # image spinner
        if (self.imageSpinner is not None):
            del self.imageSpinner
        self.imageSpinner = ImageSpinner(imagePath)
        self.updateStatusBar()

        return True

    def showImage(self, image: QImage):
        self.imageLabel.setPixmap(QPixmap.fromImage(image))
        self.imageLabel.adjustSize()
        # self.fitToWindow()
        self.scaleImage()

    def open(self):
        openDialog = QFileDialog(self, "Open Image")
        self.initOpenDialog(openDialog, QFileDialog.AcceptMode.AcceptOpen)
        if openDialog.exec():
            filePath = list(openDialog.selectedFiles())[-1]
            if self.loadImage(filePath):
                self.updateActions()
                self.displayImageInfo()

    def print(self):
        QMessageBox.information(self, "ImageViewer",
                                "This is the 'print' action handler - yet to be implemented")

    def zoomIn(self):
        self.scaleImage(1.25)
        self.updateStatusBar()

    def zoomOut(self):
        self.scaleImage(0.75)
        self.updateStatusBar()

    def zoomNormal(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0
        self.updateStatusBar()

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAction.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.zoomNormal()
        self.updateActions()

    def rotateLeft(self):
        self.cv2image = cv2.rotate(self.cv2image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.image = self.openCV2QImage(self.cv2image)
        self.showImage(self.image)

    def rotateRight(self):
        self.cv2image = cv2.rotate(self.cv2image, cv2.ROTATE_90_CLOCKWISE)
        self.image = self.openCV2QImage(self.cv2image)
        self.showImage(self.image)

    def prevImage(self):
        if not self.imageSpinner.atFirstPath():
            assert (self.imageSpinner is not None)
            imagePath = self.imageSpinner.prevImagePath()
            if (self.loadImage(imagePath)):
                self.updateActions()
        else:
            QMessageBox.information(self, "ImageViewer", "Displaying first image in folder!")

    def nextImage(self):
        if not self.imageSpinner.atLastPath():
            assert (self.imageSpinner is not None)
            imagePath = self.imageSpinner.nextImagePath()
            if (self.loadImage(imagePath)):
                self.updateActions()
        else:
            QMessageBox.information(self, "ImageViewer", "Displaying last image in folder!")

    def about(self):
        QMessageBox.about(self, "About Image Viewer",
                          f"<b>Image Viewer</b> application to view images on desktop.<br/>"
                          f"Developed with PyQt {PYQT_VERSION_STR} and Chocolaf theme<br/><br/>"
                          f"Version 1.0, by Manish Bhobe<br/>"
                          f"Free to use, but use at your own risk!!")


def main():
    ap = ArgumentParser()
    ap.add_argument("-i", "--image", required=False,
                    help="Full path to image")
    args = vars(ap.parse_args())

    app = ChocolafApp(sys.argv)
    app.setStyle("Chocolaf")

    w = ImageViewer()
    w.setWindowTitle(f"PyQt {PYQT_VERSION_STR} Image Viewer")
    if args['image'] is not None:
        # check if image path provided
        if os.path.exists(args['image']):
            w.loadImage(args['image'])
        else:
            print(f"WARNING: {args['image']} - path does not exist!")
    w.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
