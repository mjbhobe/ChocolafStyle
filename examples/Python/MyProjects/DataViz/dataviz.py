#!/usr/bin/env python

"""
* dataviz.py: data visualization with Python & Qt
* @author (Chocolaf): Manish Bhobe
*
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import os
import sys
import argparse
import pandas as pd

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from chocolaf.utils.chocolafapp import ChocolafApp
from chocolaf.palettes import ChocolafPalette


def transform_date(utc_time, timezone=None):
    utc_fmt = "yyyy-MM-ddTHH:mm:ss.zzzZ"
    new_date = QDateTime().fromString(utc_time, utc_fmt)
    if timezone:
        new_date.setTimeZone(timezone)
        #print(f"{new_date.toString('dd-MMMM-yyyy hh:mm:ss ap')} - {new_date.toString(Qt.SystemLocaleShortDate)}")
    return new_date.toString('dd-MMM-yy hh:mm:ss ap')


def read_data(data_file_path):
    if os.path.exists(data_file_path):
        df = pd.read_csv(data_file_path)
        # drop all rows where magnitude < 0
        df = df.drop(df[df.mag < 0].index)
        magnitudes = df["mag"]
        # avaiableTZs = QTimeZone.availableTimeZoneIds(QLocale.UnitedStates)
        # print(avaiableTZs)
        # our timezone
        timezone = QTimeZone(b"Asia/Kolkata")
        # get timestamp transformed into our timezone
        times = df["time"].apply(lambda x: transform_date(x, timezone))
        return times, magnitudes
    else:
        
        raise ValueError(f"Invalid path! {data_file_path} - does not exist.")


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super(CustomTableModel, self).__init__()
        if data is not None:
            self.load_data(data)

    def load_data(self, data):
        self.input_dates = data[0].values
        self.input_magnitudes = data[1].values
        self.column_count = 2
        self.row_count = len(self.input_magnitudes)

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("Date", "Magnitude")[section]
        else:
            return f"{section}"

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if column == 0:
                raw_date = self.input_dates[row]
                date = f"{raw_date}"
                return date[:-3]
            elif column == 1:
                return "{:.2f}".format(self.input_magnitudes[row])
        elif role == Qt.BackgroundRole:
            return ChocolafPalette.Window_Color  # QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None


class Widget(QWidget):
    def __init__(self, data):
        QWidget.__init__(self)

        # Getting the Model
        self.model = CustomTableModel(data)

        # Creating a QTableView
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        # QTableView Headers
        self.horizontal_header = self.table_view.horizontalHeader()
        self.vertical_header = self.table_view.verticalHeader()
        self.horizontal_header.setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.vertical_header.setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        # self.horizontal_header.setStretchLastSection(True)

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Left layout
        size.setHorizontalStretch(1)
        self.table_view.setSizePolicy(size)
        self.main_layout.addWidget(self.table_view)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)


class MainWindow(QMainWindow):
    def __init__(self, widget, parent: QWidget = None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("Eartquakes information")
        self.setCentralWidget(widget)

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(qApp.exit)

        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Data loaded and plotted")

        # Window dimensions
        geometry = qApp.desktop().availableGeometry(self)
        self.setFixedSize(int(geometry.width() * 0.8), int(geometry.height() * 0.7))


def main():
    argsParser = argparse.ArgumentParser()
    argsParser.add_argument("-f", "--file", required=True,
                            help="Enter path of data file", type=str)
    args = argsParser.parse_args()
    data_file_path = args.file
    data = read_data(data_file_path)

    app = ChocolafApp(sys.argv)
    app.setStyle("Chocolaf")

    widget = Widget(data)
    window = MainWindow(widget)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
