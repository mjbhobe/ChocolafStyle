#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ImageEditor.py: Image editor application with PyQt and OpenCV
import os
import pathlib
import sys
from argparse import ArgumentParser
import cv2

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from chocolaf.utils.chocolafapp import ChocolafApp
from ImageSpinner import ImageSpinner
import ImageEditor_rc


class ImageEditor(QMainWindow):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.imageLoaded = False
        self.imageLabel = QLabel("")
        self.imageCountLabel = QLabel("")
        self.scaleFactorLabel = QLabel("")
        self.imageInfoLabel = QLabel("")
        self.scrollArea = QScrollArea()
        self.cv2image = None       # openCV image
        self.image = None          # converted to qimage
        self.scaleFactor = 1.0
        self.firstDialog = True
        self.imageSpinner = None
        self.setupUi()

    def setupUi(self):
        # self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} Image Editor")
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
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
            f"Image Editor: developed with PyQt {PYQT_VERSION_STR} by Manish Bhobe")
        self.setupStatusBar()

        self.resize(QGuiApplication.primaryScreen().availableSize() * (4 / 5))
        self.setWindowIcon(QIcon(":/app_icon.png"))

    def createActions(self) -> None:
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

        self.blurAction = QAction("&Blur Image", self)
        self.blurAction.setIcon(QIcon(":/blur.png"))
        self.blurAction.setStatusTip("Blue active image")
        self.blurAction.triggered.connect(self.blurImage)
        self.blurAction.setEnabled(False)

        self.sharpenAction = QAction("&Sharpen Image", self)
        self.sharpenAction.setIcon(QIcon(":/sharpen.png"))
        self.sharpenAction.setStatusTip("Sharpen active image")
        self.sharpenAction.triggered.connect(self.sharpenImage)
        self.sharpenAction.setEnabled(False)

        self.erodeAction = QAction("&Erode Image", self)
        self.erodeAction.setIcon(QIcon(":/erode.png"))
        self.erodeAction.setStatusTip("Erode active image")
        self.erodeAction.triggered.connect(self.erodeImage)
        self.erodeAction.setEnabled(False)

        self.cartoonAction = QAction("&Cartoonify Image", self)
        self.cartoonAction.setIcon(QIcon(":/cartoon.png"))
        self.cartoonAction.setStatusTip("Cartoonify active image")
        self.cartoonAction.triggered.connect(self.cartoonifyImage)
        self.cartoonAction.setEnabled(False)

        # View category...
        self.zoomInAction = QAction("Zoom &in (25%)", self)
        self.zoomInAction.setShortcut(QKeySequence("Ctrl++"))
        self.zoomInAction.setIcon(QIcon(":/zoom_in.png"))
        self.zoomInAction.setStatusTip("Zoom into the image by 25%")
        self.zoomInAction.triggered.connect(self.zoomIn)
        self.zoomInAction.setEnabled(False)

        self.zoomOutAction = QAction("Zoom &out (25%)", self)
        self.zoomOutAction.setShortcut(QKeySequence("Ctrl++"))
        self.zoomOutAction.setIcon(QIcon(":/zoom_out.png"))
        self.zoomOutAction.setStatusTip("Zoom out of the image by 25%")
        self.zoomOutAction.triggered.connect(self.zoomOut)
        self.zoomOutAction.setEnabled(False)

        self.zoomNormalAction = QAction("&Normal size", self)
        self.zoomNormalAction.setShortcut(QKeySequence("Ctrl+0"))
        # self.zoomNormalAction.setIcon(QIcon("./images/zoom_out.png"))
        self.zoomNormalAction.setStatusTip("Zoom to normal size")
        self.zoomNormalAction.triggered.connect(self.zoomNormal)
        self.zoomNormalAction.setEnabled(False)

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
        self.aboutQtAction.setStatusTip("Display information about Qt library being used")
        self.aboutQtAction.triggered.connect(QApplication.instance().aboutQt)

    def createMenu(self) -> None:
        # file menu
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.printAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

        # edit menu
        editMenu = self.menuBar().addMenu("&Effects")
        editMenu.addAction(self.blurAction)
        editMenu.addAction(self.sharpenAction)
        editMenu.addAction(self.erodeAction)
        editMenu.addAction(self.cartoonAction)

        # view menu
        viewMenu = self.menuBar().addMenu("View")
        viewMenu.addAction(self.zoomInAction)
        viewMenu.addAction(self.zoomOutAction)
        # viewMenu.addAction(self.zoomNormalAction)
        viewMenu.addSeparator()
        viewMenu.addAction(self.fitToWindowAction)
        viewMenu.addSeparator()
        viewMenu.addAction(self.prevImageAction)
        viewMenu.addAction(self.nextImageAction)

        # help menu
        helpMenu = self.menuBar().addMenu("Help")
        helpMenu.addAction(self.aboutAction)
        helpMenu.addAction(self.aboutQtAction)

    def createToolbar(self) -> None:
        toolBar = self.addToolBar("Main")
        toolBar.addAction(self.openAction)
        toolBar.addAction(self.printAction)
        toolBar.addSeparator()
        toolBar.addAction(self.blurAction)
        toolBar.addAction(self.sharpenAction)
        toolBar.addAction(self.erodeAction)
        toolBar.addAction(self.cartoonAction)
        toolBar.addSeparator()
        toolBar.addAction(self.zoomInAction)
        toolBar.addAction(self.zoomOutAction)
        toolBar.addAction(self.fitToWindowAction)
        toolBar.addAction(self.prevImageAction)
        toolBar.addAction(self.nextImageAction)

    def updateActions(self) -> None:
        self.fitToWindowAction.setEnabled(not (self.image is None))
        self.blurAction.setEnabled(not (self.image is None))
        self.sharpenAction.setEnabled(not (self.image is None))
        self.erodeAction.setEnabled(not (self.image is None))
        self.cartoonAction.setEnabled(not (self.image is None))

        self.zoomInAction.setEnabled(not self.fitToWindowAction.isChecked())
        self.zoomOutAction.setEnabled(not self.fitToWindowAction.isChecked())
        self.zoomNormalAction.setEnabled(not self.fitToWindowAction.isChecked())
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

    def displayImageInfo(self) -> None:
        if self.image.isNull():
            return
        print(f"Image info -> width: {self.image.width()} - height: {self.image.height()} " +
              f"- bits/pixel: {self.image.depth()}")

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

    def adjustScrollbar(self, scrollBar: QScrollBar, factor: float):
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
        if acceptMode == QFileDialog.AcceptMode.AcceptSave:
            dialog.setDefaultSuffix("jpg")

    def loadImage(self, imagePath: str) -> bool:
        assert os.path.exists(imagePath), f"FATAL: could not load file {imagePath}"
        # reader = QImageReader(imagePath)
        # reader.setAutoTransform(True)
        # self.image = reader.read()
        # if self.image is None:
        #     QMessageBox.error(self, "ImageEditor", f"Could not load {imagePath}")
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

        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} Image Editor: {imagePath}")

        # image spinner
        if self.imageSpinner is not None:
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
        QMessageBox.information(self, "ImageEditor",
                                "This is the 'print' action handler - yet to be implemented")

    def blurImage(self):
        self.cv2image = cv2.blur(self.cv2image, ksize=(8, 8))
        self.image = self.openCV2QImage(self.cv2image)
        self.showImage(self.image)
        #print("Will blur active image")

    def sharpenImage(self):
        self.cv2image = cv2.GaussianBlur(self.cv2image, ksize=(9, 9), sigmaX=0.0,
                                         sigmaY=0.0, borderType=4)
        self.image = self.openCV2QImage(self.cv2image)
        self.showImage(self.image)
        # print("Will sharpen active image")

    def erodeImage(self):
        print("Will erode active image")

    def cartoonifyImage(self):
        print("Will cartoonify active image")

    def zoomIn(self) -> None:
        self.scaleImage(1.25)
        self.updateStatusBar()

    def zoomOut(self) -> None:
        self.scaleImage(0.75)
        self.updateStatusBar()

    def zoomNormal(self) -> None:
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0
        self.updateStatusBar()

    def fitToWindow(self) -> None:
        fitToWindow = self.fitToWindowAction.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.zoomNormal()
        self.updateActions()

    def prevImage(self):
        if not self.imageSpinner.atFirstPath():
            assert (self.imageSpinner is not None)
            imagePath = self.imageSpinner.prevImagePath()
            if self.loadImage(imagePath):
                self.updateActions()
        else:
            QMessageBox.information(self, "ImageEditor", "Displaying first image in folder!")

    def nextImage(self):
        if not self.imageSpinner.atLastPath():
            assert (self.imageSpinner is not None)
            imagePath = self.imageSpinner.nextImagePath()
            if self.loadImage(imagePath):
                self.updateActions()
        else:
            QMessageBox.information(self, "ImageEditor", "Displaying last image in folder!")

    def about(self):
        QMessageBox.about(self, "About Image Editor",
                          f"<b>Image Editor</b> application to view images & apply simple effects.<br/>"
                          f"Developed with PyQt {PYQT_VERSION_STR} and Chocolaf theme<br/><br/>"
                          f"Version 1.0, by Manish Bhobe<br/>"
                          f"Free to use, but use at your own risk!!")


def main():
    ap = ArgumentParser()
    ap.add_argument("-i", "--image", required=False,
                    help="Full path to image")
    args = vars(ap.parse_args())
    app = ChocolafApp(sys.argv)

    w = ImageEditor()
    w.setWindowTitle(f"PyQt {PYQT_VERSION_STR} Image Editor")
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
