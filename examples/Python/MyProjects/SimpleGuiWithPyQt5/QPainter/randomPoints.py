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
Window_Title = f"PyQt {PYQT_VERSION_STR} QPainter - random points"

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
        self.canvas = QPixmap(640, 480)
        self.canvas.fill(ChocolafPalette.Window_Color)
        self.label.setPixmap(self.canvas)
        self.setCentralWidget(self.label)
        self.setWindowTitle(Window_Title)
        self.setWindowIcon(QIcon(os.path.join(App_Path, "painter_icon.png")))

    def drawSomething(self, painter: QPainter) -> None:
        # get center of client area
        rc = self.rect()
        x0, y0 = rc.width() // 2, rc.height() // 2
        colors = ['#FFD141', '#376F9F', '#0D1F2D', '#E9EBEF', '#EB5160']
        pen = QPen()
        pen.setWidth(3)
        painter.setPen(pen)

        for n in range(10000):
            pen.setColor(QColor(random.choice(colors)))
            painter.setPen(pen)
            painter.drawPoint(
                x0 + random.randint(-(x0 + 1), (x0 - 1)),
                y0 + random.randint(-(y0 + 1), (y0 - 1)),
            )

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self.label.pixmap())
        painter.setRenderHint(QPainter.Antialiasing, True)
        self.drawSomething(painter)
        painter.end()


if __name__ == "__main__":
    app = ChocolafApp(sys.argv)
    # app.setStyle("Fusion")
    app.setStyle("Chocolaf")

    win = MainWindow()
    win.show()

    sys.exit(app.exec())
