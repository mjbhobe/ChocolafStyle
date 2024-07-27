""" plot.py - plot stock prices using plotting libraries """

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import datetime


sns.set(font_scale=0.9)

plt.style.use("seaborn-v0_8-dark-palette")
# print(plt.style.available)
# sys.exit(-1)

START_DATE, END_DATE = "2000-01-01", "2024-06-30"
SYMBOLS = ["AAPL"]
TICKER = "RELIANCE.NS"


def download_stock_prices(
    symbol=TICKER,
    start_date=START_DATE,
    end_date=END_DATE,
) -> pd.DataFrame:
    # download AAPL stock price
    msft_df = yf.download(
        symbol,  # one stock or list of stock symbols ['AAPL','MSFT','AMZN']
        start=start_date,  # from date
        end=end_date,  # to date
        # auto_adjust=True,     # adjust OHLC automatically?
        # actions=True,         # download dividends & stock splits
        # interval="1d",        # Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo Intraday data cannot extend last 60 days
        progress=False,
    )
    msft_df.rename(columns={"Adj Close": "Adj_Close"}, inplace=True)
    print(msft_df.tail())
    return msft_df


# convert the price to returns
""" 
stock prices are usually non-stationary, which means that their means & variance change
over time. For any time-series analysis, stock data series must be stationary. Hence we
convert the stock prices to returns, which have constant mean & variance over time.
We have various types of returns
    Simple returns: aggregate over assets; simple returns of a portfolio is the weighted 
      sum of returns of individual assets in the portfolio. 
      It is calculated using formula below
            R[t] = (P[t] - P[t-1]) / P[t-1] = (P[t] / P[t-1]) - 1
    Log returns: aggregate over time & is calculated using formula below
            r[t] = log(P[t] / P[t-1]) = log(P[t]) - log(P[t-1])
    where P[t] is price of the asset at any time 't' - above formulae do not consider dividends!
Best practice when using stock prices is to use adjusted values, which take into
account variations due to stock-split, dividends etc. (also called Corporate Actions)
"""


def valid_date(s: str) -> datetime.datetime:
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Not a valid date: {s!r}")


def main():
    # parse command line arguments
    parser = argparse.ArgumentParser()
    # on command line pass --zoom 1.2 to increase font size by 20%
    parser.add_argument(
        "--symbol",
        type=str,
        default="RELIANCE.NS",
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

    # calculate the returns on Adj close price
    print(f"Downloading {args.symbol} data from {args.start_date} to {args.end_date}")
    msft_df = download_stock_prices(args.symbol, args.start_date, args.end_date)
    df = msft_df.loc[:, ["Adj_Close"]]
    # pandas has the formula for simple returns as below
    df["Simple_Rtn"] = df.Adj_Close.pct_change()
    df["Log_Rtn"] = np.log(df.Adj_Close / df.Adj_Close.shift(1))
    print(df.head())

    # plot the data using traditional Matplotlib calls
    fig, ax = plt.subplots(3, 1, figsize=(24, 20), sharex=True)
    df.Adj_Close.plot(ax=ax[0])
    ax[0].set(
        title=f"{args.symbol} time series: {args.start_date} - {args.end_date}",
        ylabel="Stock Price (INR)",
    )
    df.Simple_Rtn.plot(ax=ax[1])
    ax[1].set(ylabel="Simple Returns (%)")
    df.Log_Rtn.plot(ax=ax[2])
    ax[2].set(xlabel="Date", ylabel="Log Returns (%)")
    plt.show()

    # using cufflinks & plotly
    import cufflinks as cf
    from plotly.offline import iplot, init_notebook_mode

    # set up configuration (run it once)
    # cf.set_config_file(world_readable=True, theme='pearl', offline=True)
    # df.iplot(
    #     subplots=True,
    #     shape=(3, 1),
    #     shared_xaxes=True,
    #     title=f"MSFT time series: {START_DATE} - {END_DATE}",
    # )
    # nit_notebook_mode()


if __name__ == "__main__":
    main()
