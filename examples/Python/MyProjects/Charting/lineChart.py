#!/usr/bin/env python
"""
* lineChart.py: displays line chart of a stock's closing price
* @author (Chocolaf): Manish Bhobe
*
* PyQt demo code taken from https://github.com/baoboa/pyqt5/tree/master/examples/widgets
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *

# sys.path.append(os.path.join(pathlib.Path(__file__).absolute().parents[2], 'common_files'))
# from pyqt5_utils import ChocolafApp
from chocolaf.palettes import ChocolafPalette
from chocolaf.utils.chocolafapp import ChocolafApp

import yfinance
import pandas as pd
from datetime import datetime, timedelta, date

# some global constants
START_DATE = '2000-01-01'
END_DATE = '2022-07-31'
STOCKS = ['BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'DIVISLAB.NS', 'DIXON.NS', 'HDFCBANK.NS', 'HEROMOTOCO.NS',
          'INFY.NS', 'LT.NS', 'PIDILITIND.NS', 'RELIANCE.NS', 'SUNPHARMA.NS', 'TCS.NS', 'TITAN.NS', 'ULTRACEMCO.NS']

# download RELIANCE stock prices from NSE


def download_datasets(stocks_list=STOCKS, start_date=START_DATE, end_date=END_DATE):
    for stock in stocks_list:
        print(f"Downloading {stock} data from {start_date} to {end_date}...", flush=True)
        stock_df = yfinance.download(stock, start=start_date, end=end_date, progress=False)
        stock_df.to_csv(f'{os.path.dirname(__file__)}/data/{stock[1:] if stock.startswith("^") else stock}.csv')


def datetime_to_float(d):
    epoch = datetime.utcfromtimestamp(0)
    total_seconds = (d - epoch).total_seconds()
    # total_seconds will be in decimals (millisecond precision)
    return total_seconds


def float_to_datetime(fl):
    return datetime.fromtimestamp(fl)


def getDefaultDateRange():
    today = datetime.today()
    delta = timedelta(days=150)  # approx 5 mths
    start_date = today - delta
    start_date = date(start_date.year, start_date.month, 1)
    nextMth = 1 if today.month == 12 else today.month + 1
    nextYear = today.year + 1 if nextMth == 1 else today.year
    delta = timedelta(days=1)
    end_date = date(nextYear, nextMth, 1)
    end_date = end_date - delta
    return start_date, end_date


class LineChartWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super(LineChartWidget, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        filters = self.setupFilters()
        self.currStock = self.stocks_combo.currentText()
        start_date, end_date = self.start_date.date(), self.end_date.date()
        print(f"Start date: {start_date} - End date: {end_date}")
        chart = self.setupChart(self.stocks_combo.currentText(), start_date, end_date)
        self.chartView = QChartView(chart)
        layout = QVBoxLayout()
        layout.addWidget(filters)
        layout.addWidget(self.chartView)
        self.setLayout(layout)
        self.stocks_combo.currentIndexChanged.connect(self.stockChanged)

        self.setMinimumSize(1024, 650)
        self.setWindowTitle(f"PyQt{PYQT_VERSION_STR}: line chart demo")

    def setupFilters(self):
        stocks_list = sorted([stock.split('.')[0].title() for stock in STOCKS])
        self.stocks_combo = QComboBox()
        for stock in stocks_list:
            self.stocks_combo.addItem(stock)
        self.stocks_combo.setCurrentIndex(self.stocks_combo.findText("Reliance"))

        startDate, endDate = getDefaultDateRange()
        self.start_date = QDateEdit()
        self.start_date.setDate(startDate)
        self.end_date = QDateEdit()
        self.end_date.setDate(endDate)
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Select stock to view:"))
        layout.addWidget(self.stocks_combo)
        layout.addStretch()
        layout.addWidget(QLabel("Start Date:"))
        layout.addWidget(self.start_date)
        # layout.addStretch()
        layout.addWidget(QLabel("End Date:"))
        layout.addWidget(self.end_date)
        filtersWidget = QWidget()
        filtersWidget.setLayout(layout)
        return filtersWidget

    def stockChanged(self):
        selected_stock = self.stocks_combo.currentText()
        if selected_stock != self.currStock:
            start_date, end_date = self.start_date.date(), self.end_date.date()
            chart = self.setupChart(selected_stock, start_date, end_date)
            self.chartView.setChart(chart)
            self.currStock = selected_stock

    def setupChart(self, stock_name, start_date, end_date):
        chart = QChart()
        start_date_str, end_date_str = start_date.toString('yyyy-MM-dd'), end_date.toString('yyyy-MM-dd')
        chart.setTitle(
            f"<html><b>{stock_name.title()}</b> Closing Price from <b>{start_date.toString('dd-MMM-yy')}</b> " +
            f"to <b>{end_date.toString('dd-MMM-yy')}</b></html>")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().hide()

        stock_df = pd.read_csv(f'{os.path.dirname(__file__)}/data/{stock_name.upper()}.NS.csv')
        # stock_df['Date'] = pd.to_datetime(stock_df['Date'])
        date_mask = ((stock_df['Date'] >= start_date_str) & (stock_df['Date'] <= end_date_str))
        stock_df2 = stock_df.loc[date_mask]

        xVals = stock_df2['Date'].values
        yVals = stock_df2['Close'].values
        minY, maxY = yVals.min() - 20, yVals.max() + 20
        print(f"xVals.min() {xVals.min()} - xVals.max() {xVals.max()}")
        print(f"yVals.min() {minY} - yVals.max() {maxY}")

        # setup the line series
        series = QLineSeries()
        for idx in range(len(xVals)):
            xVal: QDateTime = QDateTime()
            xVal.setDate(datetime.strptime(xVals[idx], "%Y-%m-%d"))
            series.append(xVal.toMSecsSinceEpoch(), yVals[idx])
        chart.addSeries(series)

        # setup the axis
        xAxis = QDateTimeAxis()
        xAxis.setFormat("yy-MM-dd")
        xAxis.setTickCount(10)
        range_start, range_end = QDateTime(), QDateTime()
        range_start.setDate(datetime.strptime(xVals[0], "%Y-%m-%d"))
        range_start.setDate(datetime.strptime(xVals[-1], "%Y-%m-%d"))
        xAxis.setRange(range_start, range_end)
        chart.addAxis(xAxis, Qt.AlignBottom)
        series.attachAxis(xAxis)

        # setup the axis
        yAxis = QValueAxis()
        yAxis.setLabelFormat("%.2f")
        yAxis.setTickCount(10)
        yAxis.setRange(minY, maxY)
        chart.addAxis(yAxis, Qt.AlignLeft)
        series.attachAxis(yAxis)

        return chart


if __name__ == "__main__":
    # re-run the following line if you want to download stocks data
    # download_datasets(start_date=START_DATE, end_date=END_DATE)
    # sys.exit(-1)

    stocks_list = [stock.split('.')[0].title() for stock in STOCKS]
    print(f"We have data for {stocks_list}")
    stock_df = pd.read_csv(f'{os.path.dirname(__file__)}/data/RELIANCE.NS.csv')
    print(stock_df.head())

    app = QApplication(sys.argv)
    win = LineChartWidget()
    win.show()
    sys.exit(app.exec())
