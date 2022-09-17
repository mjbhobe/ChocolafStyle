# -*- coding: utf-8 -*-
"""
// ============================================================================
// doodle.py: class to represent the doodle (a collection of squiggles)
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
from squiggle import Squiggle

class Doodle(QObject):
    """
    class to manage the doodle
    """
    def __init__(self, defPenWidth=3, defPenColor=QColor(qRgb(0, 65, 255))):
        super(QObject, self).__init__()
        self.__squiggles = []
        self.__defPenWidth = 1
        self.__defPenColor = QColor(qRgb(0,0,0))
        self.__modified = False
        # set default properties
        self.defPenWidth = defPenWidth
        self.defPenColor = defPenColor
        
    @property
    def modified(self):
        return self.__modified
    
    @modified.setter
    def modified(self, isModified):
        self.__modified = isModified
        
    @property
    def defPenWidth(self):
        return self.__defPenWidth
    
    @defPenWidth.setter
    def defPenWidth(self, newWidth):
        penWidth = min(max(2, newWidth), 12)
        if (newWidth < 2) or (newWidth > 12):
            qDebug(f"WARNING: incorrect value for defPenWidth ({newWidth}). Expecting value between 2 & 12. Set to {penWidth}")
        if self.__defPenWidth != penWidth:
            self.__defPenWidth = penWidth
            
    @property
    def defPenColor(self):
        return self.__defPenColor
    
    @defPenColor.setter
    def defPenColor(self, penColor : QColor) -> None:
        if self.defPenColor != penColor:
            self.__defPenColor = penColor
            
    @property
    def numSquiggles(self):
        return len(self.__squiggles)
    
    def append(self, squiggle: Squiggle) -> None:
        self.__squiggles.append(squiggle)
        
    def clear(self):
        self.__squiggles = []
        
    def draw(self, painter: QPainter) -> None:
        # doodle has it's own method to draw on QPainter
        if self.numSquiggles > 0:
            for squiggle in self.__squiggles:
                squiggle.draw(painter)



                
    

        
        
    

