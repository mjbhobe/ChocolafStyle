#!/usr/bin/env python
"""
* stackedBarChart.py - shows two stacked bar charts for min & max temps
* @author (Chocolaf): Manish Bhobe
*
* PyQt demo code taken from https://github.com/baoboa/pyqt5/tree/master/examples/widgets
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import os
import pathlib
import sys
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *

# sys.path.append(os.path.join(pathlib.Path(__file__).absolute().parents[2], 'common_files'))
# from pyqt5_utils import ChocolafApp
from chocolaf.palettes import ChocolafPalette
from chocolaf.utils.chocolafapp import ChocolafApp


class StackedBarChartWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super(StackedBarChartWidget, self).__init__(parent)

        self.lows = QBarSet("Lows")
        self.highs = QBarSet("Highs")

        for temp in [-52, -50, -45.3, -37.0, -25.6, -8.0, -6.0, -11.8, -19.7, -32.8, -43.0, -48.0]:
            self.lows.append(temp)
        for temp in [11.9, 12.8, 18.5, 26.5, 32.0, 34.8, 38.2, 34.8, 29.8, 20.4, 15.1, 11.8]:
            self.highs.append(temp)

        series = QStackedBarSeries()
        series.append(self.lows)
        series.append(self.highs)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("<html>Temperatures in &deg;C</html>")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        xAxis = QBarCategoryAxis()
        xAxis.append(categories)
        xAxis.setTitleText("Month")
        chart.addAxis(xAxis, Qt.AlignmentFlag.AlignBottom)

        yAxis = QValueAxis()
        yAxis.setRange(-52.0, 52.0)
        yAxis.setTitleText("<html>Temp &deg;C</html>")
        chart.addAxis(yAxis, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(xAxis)
        series.attachAxis(yAxis)

        chart.legend().show()
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.RenderHint.Antialiasing)

        layout = QVBoxLayout()
        layout.addWidget(chartView)
        self.setLayout(layout)

        self.setWindowTitle(f"PyQt{PYQT_VERSION_STR}: Stacked Chart Example")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    chart = StackedBarChartWidget()
    chart.resize(640, 480)
    chart.show()

    sys.exit(app.exec())
