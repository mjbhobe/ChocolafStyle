# -*- coding: utf-8 -*-
"""
* randomPoints.py - random points in client area of window
* 
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!

"""
import sys
import os
import random

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from chocolaf.palettes import ChocolafPalette
from chocolaf.utils.chocolafapp import ChocolafApp

App_Path = os.path.dirname(__file__)
Window_Title = f"PyQt {PYQT_VERSION_STR} QPainter - mouse draw"

# add some custom styling above & beyond stysheet set
style_sheet = """
    QLabel#CanvasLabel {
        border: 2px dashed rgb(102, 102, 102);
    }
    QLabel {
        qproperty-alignment: AlignCenter;
    }
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.canvas = QPixmap(800, 600)
        self.canvas.fill(ChocolafPalette.Window_Color)
        self.label.setPixmap(self.canvas)
        self.setCentralWidget(self.label)
        self.setWindowTitle(Window_Title)
        self.setWindowIcon(QIcon(os.path.join(App_Path, "painter_icon.png")))
        self.dragging = False
        self.old_x, self.old_y = 0, 0
        self.pen = QPen(ChocolafPalette.WindowText_Color, 2)
        self.label.setMouseTracking(True)

    def mousePressEvent(self, e: QMouseEvent):
        self.dragging = True
        self.old_x, self.old_y = e.pos().x(), e.pos().y()
        e.accept()

    def mouseReleaseEvent(self, e: QMouseEvent):
        self.dragging = False
        e.accept()

    def mouseMoveEvent(self, e: QMouseEvent):
        if ((e.buttons() == Qt.LeftButton) and (self.dragging)):
            painter = QPainter(self.label.pixmap())
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


if __name__ == "__main__":
    app = ChocolafApp(sys.argv)
    # app.setStyle("Fusion")
    app.setStyle("Chocolaf")

    win = MainWindow()
    win.show()

    sys.exit(app.exec())
