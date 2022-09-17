# -*- coding: utf-8 -*-
"""
// ============================================================================
// squiggle.py: represents one squiggle in the Doodle, with its own color & width
//
// Tutorial - PyQt5 Doodle Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL) 
// @author: Manish Bhobe
// My experiments with the Qt Framework. Use at your own risk!!
// ============================================================================
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Squiggle(QObject):
    """
    class for a Squiggle in the doodle
    """
    def __init__(self, penWidth=3, penColor=QColor(qRgb(0,65,255))):
        super(QObject, self).__init__()
        self.__penWidth = 1
        self.__penColor = QColor(qRgb(0,0,0))
        # the squiggle has its own pen width & color
        self.penWidth = penWidth
        self.penColor = penColor
        self.points = []

    @property
    def penWidth(self):
        return self.__penWidth

    @penWidth.setter
    def penWidth(self, penWidth):
        newWidth = min(max(2, penWidth), 12)
        if (penWidth < 2) or (penWidth > 12):
            qDebug(f"WARNING: incorrect value for penWidth ({penWidth}). Expecting value between 2 & 12. Set to {newWidth}")
        if self.penWidth != newWidth:
            self.__penWidth = newWidth

    @property
    def penColor(self):
        return self.__penColor

    @penColor.setter
    def penColor(self, penColor : QColor) -> None:
        if self.penColor != penColor:
            self.__penColor = penColor

    @property
    def numPoints(self):
        return len(self.points)

    def append(self, pt: QPoint) -> None:
        self.points.append(pt)

    def draw(self, painter: QPainter) -> None:
        # squiggle has it's own method to draw on QPainter
        if self.numPoints > 0:
            pen = QPen(self.penColor, self.penWidth)
            painter.setPen(pen)
            lastPt = None
            for i, pt in enumerate(self.points):
                if i > 0:
                    painter.drawLine(lastPt, pt)
                lastPt = pt
                


    

            
