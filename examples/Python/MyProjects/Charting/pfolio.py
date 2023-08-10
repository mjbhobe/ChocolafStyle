#!/usr/bin/env python
"""
* pfolio.py: dowload closing prices of stock portfolio
* @author (Chocolaf): Manish Bhobe
*
* PyQt demo code taken from https://github.com/baoboa/pyqt5/tree/master/examples/widgets
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import sys
import os
import pathlib
from pathlib import Path

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

import yfinance
import numpy as np
import pandas as pd
import datetime
import locale

import chocolaf
from chocolaf import ChocolafPalette

logger = chocolaf.get_logger(pathlib.Path(__file__).name)

# some pandas tweaks
pd.set_option("display.max_rows", 80)
pd.set_option("display.max_columns", 50)
pd.options.display.float_format = "{:,.2f}".format
pd.options.display.width = 1024

todays_date = datetime.datetime.now()
year, month, day = todays_date.year, todays_date.month, todays_date.day
# adjust for financial year - if today() in Jan, Feb or Mar, decrease year by 1
year = year - 1 if month in range(1, 4) else year

START_DATE = datetime.datetime(year, 4, 1)  # 01-Apr of current financial year
END_DATE = datetime.datetime.now()
logger.info(f"START_DATE = {START_DATE.strftime('%d-%b-%Y')} - END_DATE = " f"{END_DATE.strftime('%d-%b-%Y')}")

# set to India locale
locale.setlocale(locale.LC_ALL, "en_IN.utf8")


def download_stock_prices(
    holdings,
    start_date=START_DATE,
    end_date=END_DATE,
    save_path=None,
    force_download=False,
) -> pd.DataFrame:
    if (save_path is not None) and (os.path.exists(save_path)) and (not force_download):
        # if portfolio was saved before, load from save_path (if exists) unless force_download = True
        pfolio_df = pd.read_csv(save_path, index_col=0)
        logger.info(f"Portfolio loaded from {save_path}")
    else:
        # download stock prices
        logger.info("Downloading stock prices...")
        pfolio_df = pd.DataFrame()
        for symbol in holdings["PFOLIO"]:
            logger.info(f"Downloading {symbol} data from {start_date} to {end_date}...")
            stock_df = yfinance.download(symbol, start=start_date, end=end_date, progress=False)
            if len(stock_df) != 0:
                pfolio_df[symbol] = stock_df["Close"]
        pfolio_df.index = pd.to_datetime(pfolio_df.index)
        pfolio_df.index = pfolio_df.index.date
        # transpose so that stock names form the index
        pfolio_df = pfolio_df.T
        # add qty column
        pfolio_df.insert(0, "Qty", list(holdings["NUM_SHARES"]))
        # save portfolio
        pfolio_df.to_csv(f"{save_path}", header=True, index=True)
        print(f"Portfolio saved to {save_path}")
    return pfolio_df


def calculate_values(df, num_days=5):
    cols = df.columns

    df_new = df[["Qty"]]

    # calculate value of stocks for each day
    for col in cols[-num_days:]:
        df_new[col] = df[col]
        df_new[f"{col}_Value"] = df[col] * df["Qty"]
    return df_new


def build_output(entry: Path, long: bool = False):
    if long:
        size = entry.stat().st_size
        date = datetime.datetime.fromtimestamp(entry.stat().st_mtime).strftime("%d-%b-%Y %H:%M:%S")
        type = "d" if entry.is_dir() else "f"
        return f"{type} {size:>10d} {date} {entry.name}"
    return entry.name


class PandasTableModel(QAbstractTableModel):
    def __init__(self, data):
        super(PandasTableModel, self).__init__()
        self._data = data

    def data(self, index : QModelIndex, role: int):
        numRows = self.rowCount(0)  # any value for index is ok
        if index.row() == (numRows - 1):
            value = ""
            # I am on the Totals row, which does not exist in the dataset!
            # if column() is a "_Value" column, then calculate tota & display it
            colName = str(self._data.columns[index.column()]).strip()
            if colName.endswith("_Value"):
                value = self._data[colName].sum()
                logger.info(f"Sum of column {colName} is {value:,.2f}")
        else:
            # get value from dataframe
            value = self._data.iloc[index.row(), index.column()]

        # value = self._data.iloc[index.row(), index.column()]

        if role == Qt.ItemDataRole.DisplayRole:
            # special formatting for floats, ints and dates
            if isinstance(value, str):
                return "%s" % value
            if isinstance(value, datetime.datetime):
                # display dates as YYYY-MM-DD
                return value.strftime("%Y-%m-%d")
            if isinstance(value, float) or (value.dtype == np.float64):
                # format as currency using locale specific format
                return locale.currency(value, grouping=True)
            if isinstance(value, int) or (value.dtype == np.int64):
                # format with locale format
                val = f"{value:,}"
                return val
            # for all other cases, return value as-is
            return value
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            # right align ints & floats
            # or isinstance(value, int):
            if isinstance(value, str):
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignLeft
            elif (
                isinstance(value, float)
                or (value.dtype == np.float64)
                or isinstance(value, int)
                or (value.dtype == np.int64)
            ):
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight
            else:
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignLeft

    def rowCount(self, index):
        # NOTE: we specify 1 more than the number of data rows to accomodate Totals
        return self._data.shape[0] + 1

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return "%s" % str(self._data.columns[section]).strip()

            if orientation == Qt.Orientation.Vertical:
                return (
                    "TOTAL VALUE"
                    if (section == self.rowCount(0) - 1)
                    else "%s" % str(self._data.index[section]).strip()
                )


class MainWindow(QMainWindow):
    def __init__(self, dataframe: pd.DataFrame):
        super(MainWindow, self).__init__()
        self.dataframe = dataframe
        self.tableView = QTableView()
        self.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.model = PandasTableModel(self.dataframe)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.setCentralWidget(self.tableView)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    today = QDateTime.currentDateTime().toString("dd-MMM-yyyy")

    save_path = Path(__file__).absolute().parents[0] / "pfolio" / f"pfolio_{today}.csvx"

    # open holdings CSV (update this when holdings change)
    holdings = pd.read_csv(pathlib.Path(__file__).parent / "holdings.csv")
    # download holdings, if not done already
    pfolio_df = download_stock_prices(holdings, start_date=START_DATE, end_date=END_DATE, save_path=save_path)
    logger.info(pfolio_df.iloc[:, -5:].head())
    # calculate totals by day
    df_values = calculate_values(pfolio_df, 5)
    logger.info(df_values)
    save_path = Path(__file__).absolute().parents[0] / "pfolio" / f"pfolio_{today}_vals.csv"
    df_values.to_csv(save_path, index=True, header=True)

    title = f"Portfolio Performance for past 5 days"
    window = MainWindow(df_values)
    window.setWindowTitle(title)
    chocolaf.centerOnScreenWithSize(window, 0.75, 0.65)
    window.show()

    sys.exit(app.exec())
