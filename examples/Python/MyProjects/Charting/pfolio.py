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
import argparse
import pathlib
from pathlib import Path

from PyQt6.QtCore import *
from PyQt6.QtGui import *
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
# pd.options.display.max_columns = 25
pd.options.display.width = 1024

# some global constants
HOLDINGS = {
    "PFOLIO": [
        "BAJAJ-AUTO.NS", "BAJAJFINSV.NS", "COLPAL.NS", "DIXON.NS",
        "HDFCBANK.NS", "HEROMOTOCO.NS", "HDFC.NS", "INFY.NS",
        "ITC.NS", "KANSAINER.NS", "LT.NS", "M&M.NS",
        "NESTLEIND.NS", "PIDILITIND.NS", "PGHH.NS", "RELIANCE.NS",
        "TCS.NS", "TATASTEEL.NS", "TITAN.NS", "ULTRACEMCO.NS",
    ],
    "NUM_SHARES": [
        166, 530, 220, 25, 100, 25,
        50, 832, 5000, 9900, 1080,
        1440, 25, 7900, 50, 402,
        408, 2500, 50, 62,
    ],
}

todays_date = datetime.datetime.now()
year, month, day = todays_date.year, todays_date.month, todays_date.day
# adjust for financial year - if today() in Jan, Feb or Mar, decrease year by 1
year = year - 1 if month in range(1, 4) else year

START_DATE = datetime.datetime(year, 4, 1)  # 01-Apr of current financial year
END_DATE = datetime.datetime.now()
print(
    f"START_DATE = {START_DATE.strftime('%d-%b-%Y')} - END_DATE = "
    f"{END_DATE.strftime('%d-%b-%Y')}"
)
locale.setlocale(locale.LC_MONETARY, "en_IN")


def download_stock_prices(
    holdings = HOLDINGS,
    start_date = START_DATE,
    end_date = END_DATE,
    save_path = None,
    force_download = False,
):
    if (save_path is not None) and (os.path.exists(save_path)) and (not force_download):
        # if portfolio was saved before, load from save_path (if exists) unless force_download
        # is True
        pfolio_df = pd.read_csv(save_path, index_col = 0)
        logger.info(f"Portfolio loaded from {save_path}")
    else:
        # download stock prices
        print("Downloading stock prices...")
        pfolio_df = pd.DataFrame()
        for symbol in holdings["PFOLIO"]:
            logger.info(f"Downloading {symbol} data from {start_date} to {end_date}...")
            stock_df = yfinance.download(symbol, start = start_date, end = end_date, progress = False)
            if len(stock_df) != 0:
                pfolio_df[symbol] = stock_df["Close"]
        pfolio_df.index = pd.to_datetime(pfolio_df.index)
        pfolio_df.index = pfolio_df.index.date
        # transpose so that stock names form the index
        pfolio_df = pfolio_df.T
        # add qty column
        pfolio_df.insert(0, "Qty", holdings["NUM_SHARES"])
        # save portfilio
        pfolio_df.to_csv(f"{save_path}", header = True, index = True)
        print(f"Portfolio saved to {save_path}")
    return pfolio_df


def calculate_values(df, num_days = 5):
    cols = df.columns

    df_new = df[["Qty"]]

    # calculate value of stocks for each day
    for col in cols[-num_days:]:
        df_new[col] = df[col]
        df_new[f"{col}_Value"] = df[col] * df["Qty"]

    # new_col_order = ['Qty']
    # for col in cols[1:]:
    #     new_col_order.append(col)
    #     new_col_order.append(f"{col}_Value")

    # df_new = df.loc[:, new_col_order]
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

    def data(self, index, role):
        value = self._data.iloc[index.row(), index.column()]

        if role == Qt.ItemDataRole.DisplayRole:
            # special formatting for floats, ints and dates
            if isinstance(value, datetime.datetime):
                # display as YYYY-MM-DD
                return value.strftime("%Y-%m-%d")
            if isinstance(value, float) or (value.dtype == np.float64):
                # display in India currency format - all floats in
                # dataframe are currency amounts
                # @see: https://stackoverflow.com/questions/40951552/convert-an-amount-to-indian-notation-in-python
                return locale.currency(value, grouping = True)
                # return f"{value:,.2f}"
            if isinstance(value, int) or (value.dtype == np.int64):
                # format with ,
                val = f"{value:,}"
                return val
            if isinstance(value, str):
                return "%s" % value
            # for all other cases, return value as-is
            return value
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            # right align ints & floats
            # or isinstance(value, int):
            if (
                isinstance(value, float)
                or (value.dtype == np.float64)
                or isinstance(value, int)
                or (value.dtype == np.int64)
            ):
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight
            else:
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignLeft

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return "%s" % str(self._data.columns[section]).strip()

            if orientation == Qt.Orientation.Vertical:
                return "%s" % str(self._data.index[section]).strip()

        # elif role == Qt.ItemDataRole.TextAlignmentRole:

    # if orientation == Qt.Orientation.Horizontal:
    #     return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight
    # if orientation == Qt.Orientation.Vertical:
    #     return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignLeft


class MainWindow(QMainWindow):
    def __init__(self, dataframe: pd.DataFrame):
        super(MainWindow, self).__init__()
        self.dataframe = dataframe
        self.tableView = QTableView()
        self.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.model = PandasTableModel(self.dataframe)
        self.tableView.setModel(self.model)
        self.setCentralWidget(self.tableView)


if __name__ == "__main__":
    # re-run the following line if you want to download stocks data
    # download_datasets(start_date=START_DATE, end_date=END_DATE)
    # sys.exit(-1)

    # app = QCoreApplication(sys.argv)
    app = chocolaf.ChocolafApp(sys.argv)
    app.setStyle("WindowsDark")
    # app = QApplication(sys.argv)
    # app.setStyle("Fusion")

    today = QDateTime.currentDateTime().toString("dd-MMM-yyyy")

    save_path = Path(__file__).absolute().parents[0] / "pfolio" / f"pfolio_{today}.csv"

    # pfolio_df = download_stock_prices().T
    pfolio_df = download_stock_prices(
        start_date = START_DATE, end_date = END_DATE, save_path = save_path
    )
    # pfolio_df['Qty'] = HOLDINGS["NUM_SHARES"]
    print(pfolio_df.iloc[:, -5:].head())
    df_values = calculate_values(pfolio_df, 5)
    print(df_values)
    save_path = Path(__file__).absolute().parents[0] / "pfolio" / f"pfolio_{today}_vals.csv"
    df_values.to_csv(save_path, index = True, header = True)

    title = f"Portfolio Performance for past 5 days"
    window = MainWindow(df_values)
    window.setWindowTitle(title)
    chocolaf.centerOnScreenWithSize(window, 0.75, 0.65)
    window.show()

    sys.exit(app.exec())

    # save_path = Path(__file__).absolute().parents[0] / "pfolio" / f"pfolio_{today}.csv"
    # pfolio_df.to_csv(f"{save_path}")

    # print(f"Portfolio saved to {save_path}")
    # print("Displaying performance from past 5 business days...")
    # pfolio_latest_five = pfolio_df.iloc[:, -5:]
    # print(pfolio_latest_five)
    # # last business day
    # pfolio_latest_sum = pfolio_df.iloc[:, -1].sum()
    # print(f"Last portfilio value: {pfolio_latest_sum:,.3f}")

    # parser = argparse.ArgumentParser()
    # parser.add_argument("path")
    # parser.add_argument("-l", "--long", action="store_true")

    # args = parser.parse_args()
    # target_dir = Path(args.path)
    # if not target_dir.exists():
    #     print(f"Target dir {target_dir} does not exist!")
    #     sys.exit(-1)

    # for entry in target_dir.iterdir():
    #     print(build_output(entry, args.long))

    sys.exit(0)
