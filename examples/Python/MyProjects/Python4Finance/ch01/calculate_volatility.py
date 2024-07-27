""" calculate_volatility.py - calculate monthly realized volatility on AAPL stock """

import sys
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

# import seaborn as sns
from download import download_stock_prices, valid_date
from download import TICKERS as TICKERS

sns.set(context="notebook", style="whitegrid", font_scale=0.9)
print(plt.style.available)
# sys.exit(-1)

plt.style.use("seaborn-v0_8-dark-palette")


START_DATE, END_DATE = "2000-01-01", "2024-07-15"
TICKER = "PERSISTENT.NS"


def realized_volatility(x):
    return np.sqrt(np.sum(x**2))


if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    # on command line pass --zoom 1.2 to increase font size by 20%
    parser.add_argument(
        "--ticker",
        type=str,
        default=TICKER,
        help="Stock symbol to download data for (e.g. RELIANCE.NS)",
    )
    parser.add_argument(
        "--start_date",
        default=START_DATE,
        help="The Start Date - format YYYY-MM-DD",
        type=valid_date,
    )
    parser.add_argument(
        "--end_date",
        default=END_DATE,
        help="The End Date - format YYYY-MM-DD",
        type=valid_date,
    )
    args = parser.parse_args()

    print(
        f"Downloading prices for {args.ticker} from {args.start_date} to {args.end_date}"
    )
    df = download_stock_prices(args.ticker, args.start_date, args.end_date)
    print(df.tail())

    df_rv = (
        df.groupby(pd.Grouper(freq="M"))
        .apply(realized_volatility)
        .rename(columns={"Log_Rtn": "rv"})
    )
    # annualize returns
    df_rv.rv = df_rv["rv"] * np.sqrt(12)

    # display plots
    fig, ax = plt.subplots(2, 1, sharex=True)
    ax[0].plot(df)
    ax[0].set_title(
        f"{args.ticker} log returns ({args.start_date.year}-{args.end_date.year})"
    )
    ax[1].plot(df_rv)
    ax[1].set_title("Annualized realized volatility")
    plt.show()
    plt.close()
