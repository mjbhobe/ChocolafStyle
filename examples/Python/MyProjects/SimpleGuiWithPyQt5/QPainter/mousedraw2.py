# -*- coding: utf-8 -*-
"""
* mousedraw2.py - paint like application - very light version
* 
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!

"""
from re import L
import sys
import os
import random

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from chocolaf.palettes import ChocolafPalette
from chocolaf.utils.chocolafapp import ChocolafApp

App_Path = os.path.dirname(__file__)
Window_Title = f"PyQt {PYQT_VERSION_STR} QPainter - drawing with the mouse"

# add some custom styling above & beyond stysheet set
STYLE_SHEET = """
    QPushButton#ColorButton {
        min-width: 22px;
        min-height: 22px;
        background-color: %s;
    }
"""

COLORS = [
    # 17 undertones https://lospec.com/palette-list/17undertones
    '#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49',
    '#458352', '#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b',
    '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
]


class PaletteButton(QPushButton):
    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QSize(22, 22))
        self.setObjectName("ColorButton")
        self.color = color
        self.setStyleSheet(STYLE_SHEET % color)


class Canvas(QLabel):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap(800, 300)
        pixmap.fill(ChocolafPalette.Window_Color)
        self.setPixmap(pixmap)
        self.old_x, self.old_y = None, None
        self.penColor = ChocolafPalette.WindowText_Color
        self.pen = QPen(self.penColor, 4)
        self.setMouseTracking(True)

    def setPenColor(self, color):
        self.penColor = QColor(color)
        self.pen = QPen(self.penColor, 4)

    def mousePressEvent(self, e: QMouseEvent):
        self.dragging = True
        self.old_x, self.old_y = e.pos().x(), e.pos().y()
        e.accept()

    def mouseReleaseEvent(self, e: QMouseEvent):
        self.dragging = False
        e.accept()

    def mouseMoveEvent(self, e: QMouseEvent):
        if ((e.buttons() == Qt.LeftButton) and (self.dragging)):
            painter = QPainter(self.pixmap())
            try:
                painter.setRenderHint(QPainter.Antialiasing, True)
                x, y = e.pos().x(), e.pos().y()
                painter.setPen(self.pen)
                painter.drawLine(QPoint(self.old_x, self.old_y), QPoint(x, y))
                self.old_x, self.old_y = x, y
            finally:
                painter.end()
                self.update()
        else:
            e.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        w = QWidget()
        l = QVBoxLayout()

        self.canvas = Canvas()
        l.addWidget(self.canvas)
        palette = QHBoxLayout()
        self.addPaletteButtons(palette)
        l.addLayout(palette)

        w.setLayout(l)
        self.setCentralWidget(w)

        self.setWindowTitle(Window_Title)
        self.setWindowIcon(QIcon(os.path.join(App_Path, "painter_icon.png")))

    def addPaletteButtons(self, layout):
        for c in COLORS:
            b = PaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.setPenColor(c))
            layout.addWidget(b)


if __name__ == "__main__":
    app = ChocolafApp(sys.argv)
    # app.setStyle("Fusion")
    app.setStyle("Chocolaf")

    win = MainWindow()
    win.show()

    sys.exit(app.exec())
