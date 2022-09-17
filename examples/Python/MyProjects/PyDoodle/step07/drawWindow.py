# -*- coding: utf-8 -*-
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

from squiggle import Squiggle
from doodle import Doodle
from chocolaf.palettes import ChocolafPalette


class DrawWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        self.setStyleSheet("background-color: white")
        self.__doodle = Doodle()
        self.__dragging = False
        self.__currSquiggle = None
        self.setMouseTracking(True)
        self._timerID = -1  # self.startTimer(1000)

    @property
    def doodle(self):
        return self.__doodle

    def timerEvent(self, e: QTimerEvent) -> None:
        if e.timerId() == self._timerID:
            if darkdetect.isDark():
                utils.setDarkPalette(qApp)
            else:
                utils.setDarkPalette(qApp, False)

    def paintEvent(self, e: QPaintEvent) -> None:
        """ handler for paint events """
        painter = QPainter()
        try:
            width, height = self.width(), self.height()
            color = ChocolafPalette.Window_Color
            painter.begin(self)
            painter.setBrush(color)
            painter.setPen(color)
            painter.drawRect(0, 0, width, height)
            painter.setRenderHint(QPainter.Antialiasing, True)
            self.doodle.draw(painter)
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
                                                   self.doodle.defPenWidth, 2, 12)
                if ok:  # user clicked Ok on QInputDialog
                    self.doodle.defPenWidth = newWidth
            else:
                # start a new line
                #self.__currSquiggle = Squiggle(self.penWidth, self.penColor)
                self.__currSquiggle = Squiggle()
                self.__currSquiggle.penWidth = self.doodle.defPenWidth
                self.__currSquiggle.penColor = self.doodle.defPenColor
                self.doodle.append(self.__currSquiggle)
                pt = QPoint(e.pos().x(), e.pos().y())
                self.__currSquiggle.append(pt)
                self.doodle.modified = True
                self.__dragging = True
        elif e.button() == Qt.RightButton:
            if (e.modifiers() & Qt.ControlModifier):
                # if Ctrl key is also pressed with mouse press, display
                # dialog to change pen color
                newColor = QColorDialog.getColor(self.doodle.defPenColor, self)
                if newColor.isValid():
                    self.doodle.defPenColor = newColor
            else:
                self.doodle.clear()
                self.update()

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        """ handler for mouse drag (left or right button) events
            NOTE: you must call setMouseTracking(True) so window can receive mouse drag events
        """
        if (e.buttons() == Qt.LeftButton) and (self.__dragging):
            assert self.__currSquiggle != None, "FATAL: self.currLine is None, when expecting valid!"
            pt = QPoint(e.pos().x(), e.pos().y())
            self.__currSquiggle.append(pt)
            self.update()
        else:
            e.accept()

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        """ handler for mouse (left or right button) released events """
        if (e.button() == Qt.LeftButton) and (self.__dragging):
            assert self.__currSquiggle != None, "FATAL: self.currLine is None, when expecting valid!"
            pt = QPoint(e.pos().x(), e.pos().y())
            self.__currSquiggle.append(pt)
            self.__dragging = False
            self.update()
        else:
            e.accept()
