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
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle("PyQt5 Doodle - Step03: Drawing points")
        labelText = "Left click anywhere in client area to see position. Right click to clear"
        self.messageLabel = QLabel(labelText, parent=self)
        self.messageLabel.setGeometry(10, 5, 500, 50)
        self.resize(QGuiApplication.primaryScreen().availableSize() * 4 / 5)
        self.modified = False
        self.points = []

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

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        try:
            if len(self.points) > 0:
                # draw only if I have points to draw!
                font = QFont("Monospace", 10)
                painter.setFont(font)
                painter.setRenderHint(QPainter.Antialiasing, True)

                for pt in self.points:
                    pos = f"({pt.x()},{pt.y()})"
                    painter.drawText(pt.x(), pt.y(), pos)
        finally:
            painter.end()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.LeftButton:
            # user pressed left mouse button - display point where
            # the mouse left button was clicked
            pt = QPoint(e.pos().x(), e.pos().y())
            self.points.append(pt)
            self.modified = True
        elif e.button() == Qt.RightButton:
            # user pressed right mouse button - clear display of
            # previous left mouse clicks, if any
            self.points = []
            self.modified = False

        # force repaint NOW!
        self.update()
