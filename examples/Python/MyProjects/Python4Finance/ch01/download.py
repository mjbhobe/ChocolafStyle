"""download.py - download stock prices using yfinance"""

import os, sys
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
import esankhyiki

from dotenv import load_dotenv, find_dotenv
import argparse
import datetime


# print(plt.style.available)
# sys.exit(-1)

START_DATE, END_DATE = "2004-08-25", "2026-06-30"

TICKERS = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "AMZN": "Amazon",
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "PIDILITE.NS": "Pidilite Industries",
    "DIXON.NS": "Dixon",
    "PERSISTENT.NS": "Persistent Systems",
}


def plot_graph(stock_df: pd.DataFrame, symbol: str) -> None:
    # 1. Create the primary plot and the left Y-axis
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot Simple Returns on the left axis
    (line1,) = ax1.plot(
        stock_df.index,
        stock_df["Simple_Rtn"],
        color="royalblue",
        label="Simple Return",
        alpha=0.7,
    )
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Simple Returns", color="royalblue")
    ax1.tick_params(axis="y", labelcolor="royalblue")
    ax1.grid(True, linestyle="--", alpha=0.3)

    # 2. Create the secondary Y-axis sharing the same X-axis
    ax2 = ax1.twinx()

    # Plot Log Returns on the right axis
    (line2,) = ax2.plot(
        stock_df.index,
        stock_df["Log_Rtn"],
        color="crimson",
        label="Log Return",
        alpha=0.7,
        linestyle="--",  # Style distinction helps when overlaid
    )
    ax2.set_ylabel("Log Returns", color="crimson")
    ax2.tick_params(axis="y", labelcolor="crimson")

    # 3. Combine legends from both axes into a single box
    lines = [line1, line2]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper left")

    # Title and layout
    plt.title(f"{symbol} - Overlaid Return Analysis", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def plot_inflation_adjusted_returns(df_monthly: pd.DataFrame, symbol: str) -> None:
    """Plots Monthly Simple Returns, Real Returns, and the Indian Inflation Rate

    in a 3-panel stacked chart layout with a shared timeline.
    """
    # 1. Initialize a 3-row stacked canvas sharing the timeline (X-axis)
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(12, 10), sharex=True)

    fig.suptitle(
        f"{symbol} - Inflation-Adjusted Return Analysis",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )

    # --- Panel 1: Nominal Simple Returns ---
    ax1.plot(
        df_monthly.index,
        df_monthly["Simple_Rtn"],
        color="royalblue",
        label="Nominal Monthly Return",
        alpha=0.85,
    )
    ax1.set_title("Nominal Simple Returns (Monthly)", fontsize=11, loc="left")
    ax1.set_ylabel("Returns")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper left")

    # --- Panel 2: Real Returns (Inflation Decoupled) ---
    ax2.plot(
        df_monthly.index,
        df_monthly["Real_Rtn"],
        color="forestgreen",
        label="Real Return (Fisher Adjusted)",
        alpha=0.85,
    )
    ax2.set_title("Real Returns (Purchasing Power Change)", fontsize=11, loc="left")
    ax2.set_ylabel("Real Returns")
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="upper left")

    # --- Panel 3: Indian Macro Inflation Rate ---
    ax3.plot(
        df_monthly.index,
        df_monthly["Inflation_Rate"],
        color="darkorange",
        label="MoSPI Inflation Rate (MoM)",
        alpha=0.85,
        linestyle="-.",
    )
    ax3.set_title("India CPI Inflation Rate (Month-on-Month)", fontsize=11, loc="left")
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Inflation Rate")
    ax3.grid(True, linestyle="--", alpha=0.5)
    ax3.legend(loc="upper left")

    # 2. Prevent axis labels and headers from clipping
    plt.tight_layout()
    plt.show()


def valid_date(s: str) -> datetime.datetime:
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Not a valid date: {s!r}")


def download_stock_prices(
    symbol: str,
    from_date: str = START_DATE,
    to_date: str = END_DATE,
    interval: str = "1d",
) -> pd.DataFrame:
    # download stock data from Yahoo! Finance
    stock_df = yf.download(
        symbol,  # one stock or list of stock symbols ['AAPL','MSFT','AMZN']
        start=from_date,  # from date
        end=to_date,  # to date
        # NOTE: in latest version of yfinance this is True by default
        # setting it to true adjusts OHLC values, and does not have an "Adj Close" column
        auto_adjust=False,
        # actions=True,         # download dividends & stock splits
        interval=interval,
        # Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo Intraday data cannot extend last 60 days
        progress=False,
    )
    stock_df.rename(columns={"Adj Close": "Adj_Close"}, inplace=True)

    # convert the price to returns
    """ 
    stock prices are usually non-stationary, which means that their means & variance change
    over time. For any time-series analysis, data series must be stationary. Hence we
    convert the stock prices to returns, which have constant mean & variance over time.
    We have various types of returns
        - Simple returns: aggregate over assets; simple returns of a portfolio is the weighted 
           sum of returns of individual assets in the portfolio. 
           It is calculated using formula below, where P = price & R = returns
                R[t] = (P[t] - P[t-1]) / P[t-1] = (P[t] / P[t-1]) - 1
        - Log returns: aggregate over time & is calculated using formula below
                r[t] = log(P[t] / P[t-1]) = log(P[t]) - log(P[t-1])
          where P[t] is price of the asset at any time 't' - above formulae don't consider dividends!
    Best practice -> when using stock prices, is to use adjusted values, which take into
    account variations due to Corporate Actions (i.e. stock-split, dividends etc.)
    """

    # pandas has the formula for simple returns as below
    stock_df["Simple_Rtn"] = stock_df.Adj_Close.pct_change()
    stock_df["Log_Rtn"] = np.log(stock_df.Adj_Close / stock_df.Adj_Close.shift(1))
    return stock_df


"""
NOTE: for Indian stocks (like Reliance, TCS etc.), we download the CPI data from
the Ministry of Statistics and Programme Implementation (MoSPI) portal. It provides a 
Python package called "e-Sankhyiki" to fetch National Statistical Office data programmatically.

To install e-Sankhyiki use the following uv command in active env
$> uv add mospi-esankhyiki

You DO NOT require an API key to download data. CPI data is published monthly
"""


def adjust_prices_for_inflation(
    stock_df: pd.DataFrame, from_date: str, to_date: str
) -> pd.DataFrame:
    """Downloads Indian Consumer Price Index data using the official e-Sankhyiki

    API query structure, downsamples stock data to a monthly interval, and calculates
    Fisher-adjusted real returns.
    """
    # 1. Download CPI using the exact verified API dictionary format
    # Passing the dataset string, the filter dictionary, and format='df' explicitly as keyword
    raw_cpi_df = esankhyiki.get_data(
        "CPI",
        {
            "base_year": "2024",  # Evaluates active modern structural consumption habits
            "series": "Current",  # Pulls regular active monthly publishing pipeline
            # Leaving 'year' out to let the API stream the continuous timeline automatically
        },
        format="df",
    )

    # 2. Normalize timestamps and isolate index figures
    # MoSPI provides dates in the 'time_period' column (e.g. '2026-03-01' or similar format)
    raw_cpi_df["date"] = pd.to_datetime(raw_cpi_df["time_period"])

    # Extract clean series of values indexed by month-end dates
    # We drop any duplicate calendar rows if different segments are present
    cpi_series = raw_cpi_df.groupby("date")["value"].mean().sort_index()

    # 3. Establish absolute daily master tracking timeline calendar matching stock data
    df_dates = pd.DataFrame(index=pd.date_range(start=from_date, end=to_date))

    # 4. Downsample daily equity data down into matching monthly chunks
    # .ffill() handles trading gaps/weekends, .asfreq('M') snaps rows to month-end ticks
    df_monthly = df_dates.join(stock_df["Adj_Close"], how="left").ffill().asfreq("M")

    # 5. Connect macro tracker indices to portfolio logs
    df_monthly = df_monthly.join(cpi_series.rename("cpi"), how="left").ffill()

    # 6. Process nominal financial and real return vectors
    df_monthly["Simple_Rtn"] = df_monthly["Adj_Close"].pct_change()
    df_monthly["Inflation_Rate"] = df_monthly["cpi"].pct_change()

    # Fisher Equation for Real Returns: (1 + Nominal) / (1 + Inflation) - 1
    df_monthly["Real_Rtn"] = (
        (1 + df_monthly["Simple_Rtn"]) / (1 + df_monthly["Inflation_Rate"])
    ) - 1

    return df_monthly


def adjust_prices_for_inflation_us(
    stock_df: pd.DataFrame, from_date: str = START_DATE, to_date: str = END_DATE
) -> pd.DataFrame:
    # above code does not account for inflation
    """
    When doing long term analysis, we must factor in inflation, which is the
    general rise of prices level of an economy over time, which results in reduced
    purchasing power. This is why inflation should be decoupled from stock-prices.
    """

    import quandl
    import configparser
    import pathlib

    config_path = pathlib.Path(__file__).parent / "config.ini"
    config = configparser.ConfigParser()
    config.read(config_path)
    quandl.ApiConfig.api_key = os.environ["QUANDL_API_KEY"]

    # quandl.ApiConfig.api_key = config["config_keys"]["quandl.ApiConfig.api_key"]

    df_cpi = quandl.get("RATEINF/CPI_USA", start_date=from_date, end_date=to_date)
    df_cpi.rename(columns={"Value": "cpi"}, inplace=True)
    # print(df_cpi.head())

    # join the stock data with CPI
    # NOTE: CPI data is published monthly!
    df_dates = pd.DataFrame(index=pd.date_range(start=from_date, end=to_date))
    df2 = (
        df_dates.join(stock_df["Adj_Close"], how="left")
        .fillna(method="ffill")
        .asfreq("M")
    )
    df2 = df2.join(df_cpi, how="left")

    # calculate returns on Adj_Close & CPI cols
    df2["Simple_Rtn"] = df2.Adj_Close.pct_change()
    df2["Inflation_Rate"] = df2.cpi.pct_change()
    df2["Real_Rtn"] = ((1 + df2.Simple_Rtn) / (1 + df2.Inflation_Rate)) - 1
    return df2


# tester code
if __name__ == "__main__":
    _ = load_dotenv(find_dotenv())
    plt.style.use("seaborn-v0_8")
    STOCK = "TCS.NS"

    df = download_stock_prices(STOCK, START_DATE, END_DATE)  # , interval="3mo")
    print(df.tail())
    df2 = adjust_prices_for_inflation(df, START_DATE, END_DATE)
    print(df2.tail())
    plot_inflation_adjusted_returns(df, STOCK)
    # print(df2.tail())

    # plot_graph(df, STOCK)

    # plt.figure(figsize=(10, 6))
    # plt.plot(df["Simple_Rtn"], lw=2, label="Simple Returns")
    # plt.plot(df["Log_Rtn"], lw=2, label="Log Returns")
    # plt.plot(df2["Simple_Rtn"], lw=2, label="Simple Returns")
    # plt.plot(df2["Inflation_Rate"], lw=2, label="Inflation Rate")
    # plt.plot(df2["Real_Rtn"], lw=2, label="Real Returns")
    # plt.title(f"{STOCK} - Stock Returns")

    # plt.legend()
    # plt.show()
