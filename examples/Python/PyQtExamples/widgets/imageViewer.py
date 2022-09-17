"""
* imageViewer.py - simple image viewer application with Chocolaf
* @author (Chocolaf): Manish Bhobe
*
* PyQt demo code taken from https://github.com/baoboa/pyqt5/tree/master/examples/widgets
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""

#############################################################################
##
# Copyright (C) 2013 Riverbank Computing Limited.
# Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved.
##
# This file is part of the examples of PyQt.
##
# $QT_BEGIN_LICENSE:BSD$
# You may use this file under the terms of the BSD license as follows:
##
# "Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in
# the documentation and/or other materials provided with the
# distribution.
# * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
# the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
##
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
# $QT_END_LICENSE$
##
#############################################################################


import os
import sys
import platform

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *

import chocolaf
from chocolaf.utils.chocolafapp import ChocolafApp
import textEditor_rc

__version__ = "1.0.0"


class ImageViewer(QMainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()

        self.printer = QPrinter()
        self.scaleFactor = 0.0

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Base)
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createMenus()
        self.createToolBars()

        self.statusBar()

        self.setWindowTitle("Image Viewer")
        self.setWindowIcon(QIcon(":/image_viewer_icon.png"))
        self.readSettings()

    def open(self):
        picsPath = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image", picsPath[-1],
                                                  "Image Files (*.png *.tiff *.jpg *.jpeg *.svg *.bmp)")
        if fileName:
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", f"Cannot load {fileName}.")
                return

            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def readSettings(self):
        settings = QSettings("ChocoApps", "Chocolaf-ImageViewer")
        pos = settings.value("pos", QPoint(200, 200))
        size = settings.value("size", QSize(640, 480))
        self.resize(size)
        self.move(pos)

    def writeSettings(self):
        settings = QSettings("ChocoApps", "Chocolaf-ImageViewer")
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())

    def closeEvent(self, event):
        self.writeSettings()
        event.accept()

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()
        self.updateActions()

    def about(self):
        QMessageBox.about(self, "About Image Viewer",
                          f"<p>The <b>Image Viewer</b> example shows how to combine " +
                          f"QLabel and QScrollArea to display an image. QLabel is " +
                          f"typically used for displaying text, but it can also display " +
                          f"an image. QScrollArea provides a scrolling view around " +
                          f"another widget. If the child widget exceeds the size of the " +
                          f"frame, QScrollArea automatically provides scroll bars.</p>" +
                          f"<p>Version {__version__}</p>" +
                          f"<p>The example demonstrates how QLabel's ability to s cale " +
                          f"its contents (QLabel.scaledContents), and QScrollArea's " +
                          f"ability to automatically resize its contents " +
                          f"(QScrollArea.widgetResizable), can be used to implement " +
                          f"zooming and scaling features.</p>" +
                          f"<p>In addition the example shows how to use QPainter to " +
                          f"print an image.</p>" +
                          f"Using Python {platform.python_version()} - Qt {QT_VERSION_STR} - PyQt {PYQT_VERSION_STR} on {platform.system()}"
                          )

    def createActions(self):
        self.openAct = QAction(QIcon(":/file_open.png"), "&Open...", self, shortcut="Ctrl+O",
                               statusTip="Open an image file to view",
                               triggered=self.open)

        self.printAct = QAction(QIcon(":/file_print.png"), "&Print...", self, shortcut="Ctrl+P",
                                statusTip="Print the displayed image",
                                enabled=False, triggered=self.print_)

        self.exitAct = QAction(QIcon(":/on-off.png"), "E&xit", self, shortcut="Ctrl+Q",
                               statusTip="Quit the application",
                               triggered=self.close)

        self.zoomInAct = QAction(QIcon(":/zoomin.png"), "Zoom &In (25%)", self, shortcut="Ctrl++",
                                 statusTip="Zoom into the image by 25%",
                                 enabled=False, triggered=self.zoomIn)

        self.zoomOutAct = QAction(QIcon(":/zoomout.png"), "Zoom &Out (25%)", self, shortcut="Ctrl+-",
                                  statusTip="Zoom out of the image by 25%",
                                  enabled=False, triggered=self.zoomOut)

        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+0",
                                     statusTip="Zoom image to normal size",
                                     enabled=False, triggered=self.normalSize)

        self.fitToWindowAct = QAction(QIcon(":/zoom_to_fill.png"), "&Fit to Window", self, enabled=False,
                                      statusTip="Zoom image to fit the size of viewer",
                                      checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)

        self.aboutAct = QAction(
            "&About", self, statusTip="Display information about application", triggered=self.about)

        self.aboutQtAct = QAction(QIcon(":/qt_logo.png"), "About &Qt", self,
                                  statusTip="Display information about Qt Framework used",
                                  triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    def createToolBars(self):
        fileToolBar = self.addToolBar("File")
        fileToolBar.addAction(self.openAct)
        fileToolBar.addAction(self.printAct)

        viewToolBar = self.addToolBar("View")
        viewToolBar.addAction(self.zoomInAct)
        viewToolBar.addAction(self.zoomOutAct)
        viewToolBar.addAction(self.fitToWindowAct)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = ChocolafApp(sys.argv)
    app.setStyle("Chocolaf")

    win = ImageViewer()
    # win.setStyleSheet(app.getStyleSheet("Chocolaf"))
    win.move(100, 100)
    win.show()

    # rect = win.geometry()
    # win1 = Window()
    # win1.setStyleSheet(app.getStyleSheet("QDarkStyle-dark"))
    # win1.move(rect.left() + rect.width() // 4 + 20, rect.top() + rect.height() + 50)
    # win1.show()

    return app.exec()


if __name__ == "__main__":
    main()
