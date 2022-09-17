"""
* lineChart.py: draw a line chart from data in a CSV file
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
import os
import csv

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtChart import *

import chocolaf
from chocolaf.utils.chocolafapp import ChocolafApp


class DisplayGraph(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Initialize the window and display its contents."""
        self.setMinimumSize(600, 400)
        self.setWindowTitle("Ex 3.1 - Line Chart Example")
        self.setupChart()
        self.show()

    def setupChart(self):
        """Set up the GUI's graph line series type, chart instance, chart
        axes, and chart view widget."""
        # Collect x and y data values from the CSV file
        x_values, y_values = self.loadCSVFile()
        # Create chart object
        chart = QChart()
        chart.setTitle("Public Social Spending as a Share of GDP for Sweden, 1880 to 2016")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().hide()  # Hide the chart's legend
        line_series = QLineSeries()  # Using line charts for this example
        # Loop through corresponding x and y values and add them to the line chart
        for value in range(0, self.row_count - 1):
            line_series.append(x_values[value], y_values[value])
        chart.addSeries(line_series)  # Add line series to chart instance
        # Specify parameters for the x and y axes
        axis_x = QValueAxis()
        axis_x.setLabelFormat("%i")
        axis_x.setTickCount(10)
        axis_x.setRange(1880, 2016)
        chart.addAxis(axis_x, Qt.AlignBottom)
        line_series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setLabelFormat("%i" + "%")
        axis_y.setRange(0, 40)
        chart.addAxis(axis_y, Qt.AlignLeft)
        line_series.attachAxis(axis_y)

        # Create QChartView object for displaying the chart
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        # Create layout and set the layout for the window
        v_box = QVBoxLayout()
        v_box.addWidget(chart_view)
        self.setLayout(v_box)

    def loadCSVFile(self):
        """Load data from CSV file for the line chart.
        Select and store x and y values into Python list objects.
        Return the x_values and y_values lists."""

        x_values, y_values = [], []
        data_file_path = os.path.join(os.path.dirname(__file__), "social_spending_sweden.csv")
        # file_name = "./social_spending_sweden.csv"
        assert(os.path.exists(data_file_path))
        with open(data_file_path, "r") as csv_f:
            reader = csv.reader(csv_f)
            header_labels = next(reader)  # Skip header row
            for row in reader:
                x = int(row[2])
                x_values.append(x)
                y = float(row[3])
                y_values.append(y)
            # Count the number of rows in the CSV file. Reset the reader's
            # current position back to the top of the file
            csv_f.seek(0)
            self.row_count = len(list(reader))
        return x_values, y_values


if __name__ == '__main__':
    app = ChocolafApp(sys.argv)
    # app.setStyle("Chocolaf")
    # print(os.path.dirname(__file__), flush=True)

    window = DisplayGraph()
    window.show()

    sys.exit(app.exec())
