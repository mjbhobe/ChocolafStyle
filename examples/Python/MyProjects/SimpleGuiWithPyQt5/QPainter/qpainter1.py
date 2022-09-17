# -*- coding: utf-8 -*-
"""
* qpainter1.py - using QPainter for simple drawing in PyQt5
* 
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!

"""
import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from chocolaf.palettes import ChocolafPalette
from chocolaf.utils.chocolafapp import ChocolafApp

App_Path = os.path.dirname(__file__)
Window_Title = f"PyQt {PYQT_VERSION_STR} QPainter - draw simple shapes"

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
        self.label.setObjectName("CanvasLabel")
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
        pen = QPen(QColor(qRgb(120, 120, 120)), 1)
        pen.setStyle(Qt.DashLine)
        # draw axes
        painter.setPen(pen)
        painter.drawLine(x0, y0 - 250, x0, y0 + 250)
        painter.drawLine(x0 - 300, y0, x0 + 300, y0)

        pen = QPen(QColor(qRgb(0, 255, 128)), 5)
        painter.setPen(pen)
        painter.drawLine(10, 10, 300, 200)
        painter.drawRect(QRectF(QPointF(100, 100), QPointF(250, 280)))

        brush = QBrush(QColor(qRgb(0, 255, 128)), Qt.BDiagPattern)
        painter.setBrush(brush)
        painter.drawEllipse(QRectF(x0 - 100, y0 - 75, 200, 150))

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
