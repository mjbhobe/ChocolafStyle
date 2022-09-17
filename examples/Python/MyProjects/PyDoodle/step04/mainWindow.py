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
        self.setWindowTitle("PyQt5 Doodle - Step04: Drawing a Squiggle")
        self.resize(QGuiApplication.primaryScreen().availableSize() * 4 / 5)
        self.modified = False
        self.points = []
        self.dragging = False
        self.penColor = QColor(qRgb(0, 85, 255))
        self.penWidth = 3
        # enable mouse drags to send events to window
        self.setMouseTracking(True)

    # operating system Events
    def closeEvent(self, e):
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

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter()
        try:
            painter.begin(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            self.drawSquiggle(painter)
        finally:
            painter.end()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.LeftButton:
            # clear the previous squiggle
            self.points = []
            # start a new squiggle
            pt = QPoint(e.pos().x(), e.pos().y())
            #print(f"Got mousePressEvent at ({pt.x()}, {pt.y()})")
            qDebug(f"Got a Left-Mouse-Button-Pressed event at ({pt.x()}, {pt.y()})")
            self.points.append(pt)
            self.modified = True
            self.dragging = True
        elif e.button() == Qt.RightButton:
            qDebug("Got a Right-Mouse-Button-Pressed event")
            self.points = []
            self.modified = False
            self.update()

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if (e.buttons() == Qt.LeftButton) and (self.dragging):
            pt = QPoint(e.pos().x(), e.pos().y())
            #print(f"Got mouseMoveEvent event at ({pt.x()}, {pt.y()})")
            self.points.append(pt)
            self.update()
        else:
            e.accept()

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        if (e.button() == Qt.LeftButton) and (self.dragging):
            pt = QPoint(e.pos().x(), e.pos().y())
            self.points.append(pt)
            #print(f"Got mouseReleaseEvent event at ({pt.x()}, {pt.y()})")
            self.dragging = False
            self.update()
        else:
            e.accept()
