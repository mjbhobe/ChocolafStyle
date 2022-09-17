"""
// ============================================================================
// mainWindow.py: custom QMainWindow derived class for main window
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


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(QMainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("PyQt5 Doodle - Step05: Changing squiggle's width & color")
        #self.setGeometry(QRect(100, 100, 640, 480))
        self.resize(QGuiApplication.primaryScreen().availableSize() * 4 / 5)
        self.modified = False
        self.points = []
        self.dragging = False
        self.penColor = QColor(qRgb(0, 65, 255))
        self.penWidth = 3
        self.setMouseTracking(True)

    def drawSquiggle(self, painter):
        if len(self.points) > 0:
            #print(f"In drawLine() function - drawing points {self.points}")
            pen = QPen(self.penColor, self.penWidth)
            painter.setPen(pen)
            lastPt = None
            for i, pt in enumerate(self.points):
                if i > 0:
                    painter.drawLine(lastPt, pt)
                lastPt = pt

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
            painter.begin(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            self.drawSquiggle(painter)
        finally:
            painter.end()

    def getKeyModifiers(self, modifiers):
        ctrlPressed = True if modifiers & Qt.ControlModifier else False
        altPressed = True if modifiers & Qt.AltModifier else False
        shiftPressed = True if modifiers & Qt.ShiftModifier else False
        return (ctrlPressed, altPressed, shiftPressed)

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
                # clear any previous doodle(s)
                self.points = []
                # start a new doodle
                pt = QPoint(e.pos().x(), e.pos().y())
                #print(f"Got mousePressEvent at ({pt.x()}, {pt.y()})")
                self.points.append(pt)
                self.modified = True
                self.dragging = True
        elif e.button() == Qt.RightButton:
            if (e.modifiers() == Qt.ControlModifier):
                # if Ctrl key is also pressed with mouse press, display
                # dialog to change pen color
                newColor = QColorDialog.getColor(self.penColor, self)
                if newColor.isValid():
                    self.penColor = newColor
            else:
                self.points = []
                self.modified = False
                self.update()

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        """ handler for mouse drag (left or right button) events
            NOTE: you must call setMouseTracking(True) so window can receive mouse drag events
        """
        if (e.buttons() == Qt.LeftButton) and (self.dragging):
            pt = QPoint(e.pos().x(), e.pos().y())
            self.points.append(pt)
            self.update()
        else:
            e.accept()

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        """ handler for mouse (left or right button) released events """
        if (e.button() == Qt.LeftButton) and (self.dragging):
            pt = QPoint(e.pos().x(), e.pos().y())
            self.points.append(pt)
            #print(f"Got mouseReleaseEvent event at ({pt.x()}, {pt.y()})")
            self.dragging = False
            self.update()
        else:
            e.accept()
