import os, sys
import pathlib
import numpy as np
import pandas as pd
import datetime
import yfinance

holdings_path = pathlib.Path(__file__).parent / "holdings.csv"
assert os.path.exists(holdings_path), "FATAL: holdings file does not exist!"

todays_date = datetime.datetime.now()
year, month, day = todays_date.year, todays_date.month, todays_date.day
# adjust for financial year - if today() in Jan, Feb or Mar, decrease year by 1
# year = year - 1 if month in range(1, 4) else year
start_date = datetime.datetime(year-10, 4, 1)  # 01-Apr of current financial year
end_date = datetime.datetime.now()
print(f"Downloading data from {start_date:%d-%b-%Y} - {end_date:%d-%b-%Y}")
# sys.exit(-1)

holdings = pd.read_csv(str(holdings_path))
all_holdings = pd.DataFrame()
for symbol in holdings["PFOLIO"]:
    print(f"Downloading prices for {symbol}...", flush=True, end="")
    stock_df = yfinance.download(
        symbol, start=start_date, end=end_date, progress=False
    )

    if len(stock_df) != 0:
        stock_df.to_csv(f"{symbol}.csv", header=True, index=True)
        print(f"{len(stock_df)} records saved")
        # add this to all_holdings dataframe
        symb = "NIFTY" if symbol == "^NSEI" else symbol.split('.')[0]
        all_holdings[symb] = stock_df["Adj Close"]
    else:
        print(f"WARNING -> no stock data for {symbol}!")

all_holdings.to_csv("all_holdings.csv", header=True, index=True)
print("Finished downloading prices")

print(all_holdings.head())
print(all_holdings.isna().sum())
