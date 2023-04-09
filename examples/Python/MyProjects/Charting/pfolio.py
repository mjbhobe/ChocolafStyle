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
from pathlib import Path

from PyQt5.QtCore import *

import yfinance
import pandas as pd
import datetime

# some pandas tweaks
pd.set_option("display.max_rows", 80)
pd.set_option("display.max_columns", 50)
pd.options.display.float_format = '{:,.4f}'.format

# some global constants
PFOLIO = ['BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'COLPAL.NS', 'DIXON.NS', 'HDFCBANK.NS', 'HDFC.NS', 'HEROMOTOCO.NS',
          'INFY.NS', 'ITC.NS', 'KANSAINER.NS', 'LT.NS', 'M&M.NS', 'NESTLEIND.NS', 'PIDILITIND.NS', 'PGHH.NS',
          'RELIANCE.NS', 'TCS.NS', 'TATASTEEL.NS', 'TITAN.NS', 'ULTRACEMCO.NS']

todays_date = datetime.datetime.now()
year, month, day = todays_date.year, todays_date.month, todays_date.day
# adjust for financial year - if today() in Jan, Feb or Mar, decrease year by 1
year = (year - 1 if month in range(1, 4) else year)

START_DATE = datetime.datetime(year, 4, 1)  # 01-Apr of current financial year
END_DATE = datetime.datetime.now()
print(f"START_DATE = {START_DATE.strftime('%d-%b-%Y')} - END_DATE = {END_DATE.strftime('%d-%b-%Y')}")


def download_stock_prices(stocks_list = PFOLIO, start_date = START_DATE, end_date = END_DATE):
    pfolio_df = pd.DataFrame()
    for symbol in stocks_list:
        print(f"Downloading {symbol} data from {start_date} to {end_date}...", flush = True)
        stock_df = yfinance.download(symbol, start = start_date, end = end_date, progress = False)
        if len(stock_df) != 0:
            pfolio_df[symbol] = stock_df['Close']
    return pfolio_df


def build_output(entry: Path, long: bool = False):
    if long:
        size = entry.stat().st_size
        date = datetime.datetime.fromtimestamp(entry.stat().st_mtime).strftime("%d-%b-%Y %H:%M:%S")
        type = "d" if entry.is_dir() else "f"
        return f"{type} {size:>10d} {date} {entry.name}"
    return entry.name


if __name__ == "__main__":
    # re-run the following line if you want to download stocks data
    # download_datasets(start_date=START_DATE, end_date=END_DATE)
    # sys.exit(-1)

    app = QCoreApplication(sys.argv)
    today = QDateTime.currentDateTime().toString("dd-MMM-yyyy")

    pfolio_df = download_stock_prices().T
    print(pfolio_df.head())
    save_path = Path(__file__).absolute().parents[0] / "pfolio" / f"pfolio_{today}.csv"
    pfolio_df.to_csv(f"{save_path}")
    print(f"Portfolio saved to {save_path}")
    print("Displaying performance from past 5 business days...")
    pfolio_latest_five = pfolio_df.iloc[:, -5:]
    print(pfolio_latest_five)
    # last business day
    pfolio_latest_sum = pfolio_df.iloc[:, -1].sum()
    print(f"Last portfilio value: {pfolio_latest_sum:,.3f}")

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
