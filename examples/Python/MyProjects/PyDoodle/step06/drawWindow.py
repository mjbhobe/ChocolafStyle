"""
// ============================================================================
// drawWindow.py: custom QMainWindow derived class for main window
//
// Tutorial - PyQt5 Doodle Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// @author: Manish Bhobe
// My experiments with the Qt Framework. Use at your own risk!!
// ============================================================================
"""
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from squiggle import *

from chocolaf.palettes import ChocolafPalette


class DrawWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(QMainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("PyQt5 Doodle - Step06: Drawing multiple Squiggles with own pen width & color")
        self.resize(QGuiApplication.primaryScreen().availableSize() * 4 / 5)
        self.modified = False
        self.squiggles = []
        self.dragging = False
        self.penColor = QColor(qRgb(0, 65, 255))
        self.penWidth = 3
        self.currSquiggle = None
        self.setMouseTracking(True)

    def drawSquiggles(self, painter: QPainter) -> None:
        for squiggle in self.squiggles:
            squiggle.draw(painter)

    # operating system Events
    def closeEvent(self, e):
        """ called just before the main window closes """
        if self.modified:
            resp = QMessageBox.question(self, "Confirm Close",
                                        "This will close the application.\nOk to quit?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if resp == QMessageBox.Yes:
                e.accept()
            else:
                e.ignore()
        else:
            e.accept()

    def paintEvent(self, e: QPaintEvent) -> None:
        """ handler for paint events """
        painter = QPainter()
        try:
            width, height = self.width(), self.height()
            # color = QColor(53, 53, 53) if darkdetect.isDark() \
            #     else QColor(240, 240, 240)
            color = ChocolafPalette.Window_Color
            #print(f'QPalette.Window color = {color.name()}')
            painter.begin(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setBrush(color)
            painter.setPen(color)
            painter.drawRect(0, 0, width, height)
            self.drawSquiggles(painter)
        finally:
            painter.end()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        """ handler for mouse press (left or right button) events """
        if e.button() == Qt.LeftButton:
            if (e.modifiers() & Qt.ControlModifier):
                # if Ctrl key is also pressed with mouse press, display
                # dialog to change pen thickness
                newWidth, ok = QInputDialog.getInt(self, "Pen Width",
                                                   "Enter new pen width (2-12):",
                                                   self.penWidth, 2, 12)
                if ok:  # user clicked Ok on QInputDialog
                    self.penWidth = newWidth
            else:
                # start a new line
                #self.currSquiggle = Squiggle(self.penWidth, self.penColor)
                self.currSquiggle = Squiggle()
                self.currSquiggle.penWidth = self.penWidth
                self.currSquiggle.penColor = self.penColor
                self.squiggles.append(self.currSquiggle)
                pt = QPoint(e.pos().x(), e.pos().y())
                self.currSquiggle.append(pt)
                self.modified = True
                self.dragging = True
        elif e.button() == Qt.RightButton:
            if (e.modifiers() & Qt.ControlModifier):
                # if Ctrl key is also pressed with mouse press, display
                # dialog to change pen color
                newColor = QColorDialog.getColor(self.penColor, self)
                if newColor.isValid():
                    self.penColor = newColor
            else:
                for squiggle in self.squiggles:
                    squiggle = None
                self.squiggles = []
                self.modified = False
                self.update()

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        """ handler for mouse drag (left or right button) events
            NOTE: you must call setMouseTracking(True) so window can receive mouse drag events
        """
        if (e.buttons() == Qt.LeftButton) and (self.dragging):
            assert self.currSquiggle != None, "FATAL: self.currLine is None, when expecting valid!"
            pt = QPoint(e.pos().x(), e.pos().y())
            self.currSquiggle.append(pt)
            self.update()
        else:
            e.accept()

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        """ handler for mouse (left or right button) released events """
        if (e.button() == Qt.LeftButton) and (self.dragging):
            assert self.currSquiggle != None, "FATAL: self.currLine is None, when expecting valid!"
            pt = QPoint(e.pos().x(), e.pos().y())
            self.currSquiggle.append(pt)
            self.dragging = False
            self.update()
        else:
            e.accept()
