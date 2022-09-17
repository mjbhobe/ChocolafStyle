"""
* areaChart.py: illustrates an area chart using QChart
* @author (Chocolaf): Manish Bhobe
*
* PyQt demo code taken from https://github.com/baoboa/pyqt5/tree/master/examples/widgets, with changes done for
* displaying widgets using Chocolaf & other styles
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""

#############################################################################
##
# Copyright (C) 2013 Riverbank Computing Limited.
# Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved.
##
# This file is part of the examples of PyQt.
##
# $QT_BEGIN_LICENSE:BSD$
# You may use this file under the terms of the BSD license as follows:
##
# "Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in
# the documentation and/or other materials provided with the
# distribution.
# * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
# the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
##
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
# $QT_END_LICENSE$
##
#############################################################################

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *

import chocolaf
from chocolaf.utils.chocolafapp import ChocolafApp


class AreaChart(QWidget):
    def __init__(self, parent: QWidget = None):
        super(AreaChart, self).__init__(parent)
        self.initializeUi()

    def initializeUi(self):
        self.setMinimumSize(600, 400)
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} Area Chart Demo")
        self.setupChart()

    def setupChart(self):
        series0: QLineSeries = QLineSeries()
        series1: QLineSeries = QLineSeries()

        points0 = [QPointF(1, 5), QPointF(3, 7), QPointF(7, 6), QPointF(9, 7), QPointF(12, 6), QPointF(16, 7), QPointF(18, 5)]
        for point in points0:
            series0.append(point)

        points1 = [(1, 3), (3, 4), (7, 3), (8, 2), (12, 3), (16, 4), (18, 3)]
        for point in points1:
            series1.append(point[0], point[1])

        series = QAreaSeries(series0, series1)
        series.setName("Batman")
        pen = QPen(QColor("#059605"))
        pen.setWidth(3)
        series.setPen(pen)

        # fill plot with gradient
        gradient: QLinearGradient = QLinearGradient(QPointF(0, 0), QPointF(0, 1))
        gradient.setColorAt(0.0, QColor("#3cc63c"))
        gradient.setColorAt(1.0, QColor("#26f626"))
        gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
        series.setBrush(gradient)

        # setup chart
        chart: QChart = QChart()
        chart.addSeries(series)
        chart.legend().hide()   # no legend
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Batman")

        axes_x = QValueAxis()
        axes_x.setLabelFormat("%i")
        axes_x.setRange(0, 20)
        chart.addAxis(axes_x, Qt.AlignBottom)
        series.attachAxis(axes_x)

        axes_y = QValueAxis()
        axes_y.setLabelFormat("%i")
        axes_y.setRange(0, 10)
        chart.addAxis(axes_y, Qt.AlignLeft)
        series.attachAxis(axes_y)

        chartView: QChartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        layout = QVBoxLayout()
        layout.addWidget(chartView)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    chartWindow = AreaChart()
    chartWindow.show()

    sys.exit(app.exec())
