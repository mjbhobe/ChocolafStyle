#!/usr/bin/env python
"""
* areaChart.py - area chart --- batman!
* @author (Chocolaf): Manish Bhobé
*
* PyQt demo code taken from https://github.com/baoboa/pyqt5/tree/master/examples/widgets
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *

import chocolaf


class AreaChartWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super(AreaChartWidget, self).__init__(parent)

        self.series0 = QLineSeries()
        self.series1 = QLineSeries()

        self.series0.append(
            [
                QPointF(1, 5),
                QPointF(3, 7),
                QPointF(7, 6),
                QPointF(9, 7),
                QPointF(12, 6),
                QPointF(16, 7),
                QPointF(18, 5),
            ]
        )
        self.series1.append(
            [
                QPointF(1, 3),
                QPointF(3, 4),
                QPointF(7, 3),
                QPointF(8, 2),
                QPointF(12, 3),
                QPointF(16, 4),
                QPointF(18, 3),
            ]
        )
        self.series = QAreaSeries(self.series0, self.series1)
        self.series.setName("I am...Batman")
        pen = QPen(0x059605)
        pen.setWidth(3)
        self.series.setPen(pen)

        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 1))
        gradient.setColorAt(0.0, QColor(0x3CC63C))
        gradient.setColorAt(1.0, QColor(0x26F626))
        gradient.setCoordinateMode(QGradient.CoordinateMode.ObjectBoundingMode)
        self.series.setBrush(gradient)

        # create the chart
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setWindowTitle("Simple area chart")
        self.chart.createDefaultAxes()
        self.chart.axes(Qt.Orientation.Horizontal)[0].setRange(0, 20)
        self.chart.axes(Qt.Orientation.Vertical)[0].setRange(0, 10)

        chartView = QChartView(self.chart)
        chartView.setRenderHint(QPainter.RenderHint.Antialiasing)
        # chartView.resize(640, 480)

        layout = QVBoxLayout()
        layout.addWidget(chartView)
        self.setLayout(layout)
        self.setWindowTitle(f"PyQt{PYQT_VERSION_STR}: AreaChart Example")


if __name__ == "__main__":
    chocolaf.enable_hi_dpi()
    app = chocolaf.ChocolafApp(sys.argv)
    app.setStyle("Chocolaf")

    chart = AreaChartWidget()
    # chart.resize(640, 480)
    screen = app.primaryScreen()
    screenSize = screen.size()
    width, height = int(screenSize.width() * 3 / 4), int(screenSize.height() * 3 / 4)
    chart.resize(width, height)
    chart.move(100, 100)
    chart.show()

    sys.exit(app.exec())
