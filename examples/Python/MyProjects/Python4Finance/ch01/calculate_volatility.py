""" calculate_volatility.py - calculate monthly realized volatility on AAPL stock """
import sys
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

# import seaborn as sns
from download import download_stock_prices
from download import TICKERS as TICKERS

sns.set(context="notebook", style="whitegrid", font_scale=0.9)
print(plt.style.available)
# sys.exit(-1)

plt.style.use("seaborn-v0_8-dark-palette")


START_DATE, END_DATE = "2000-01-01", "2023-12-31"
TICKER = "PERSISTENT.NS"


def realized_volatility(x):
    return np.sqrt(np.sum(x**2))


if __name__ == "__main__":
    df = download_stock_prices(TICKER, START_DATE, END_DATE)
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
    ax[0].set_title(f"{TICKERS[TICKER]} log returns (2000-2023)")
    ax[1].plot(df_rv)
    ax[1].set_title("Annualized realized volatility")
    plt.show()
    plt.close()
