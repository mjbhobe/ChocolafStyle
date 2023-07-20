""" calculate_volatility.py - calculate monthly realized volatility on AAPL stock """
import sys
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# import seaborn as sns
from download import download_stock_prices

# sns.set(context="notebook", style="whitegrid")
print(plt.style.available)
# sys.exit(-1)

plt.style.use("seaborn-v0_8-dark-palette")


START_DATE, END_DATE = "2000-01-01", "2023-03-31"


def realized_volatility(x):
    return np.sqrt(np.sum(x**2))


if __name__ == "__main__":
    df = download_stock_prices("AAPL", START_DATE, END_DATE)
    print(df.tail())

    df_rv = df.groupby(pd.Grouper(freq="M")).apply(realized_volatility).rename(columns={"Log_Rtn": "rv"})
    # annualize returns
    df_rv.rv = df_rv["rv"] * np.sqrt(12)

    # display plots
    fig, ax = plt.subplots(2, 1, sharex=True)
    ax[0].plot(df)
    ax[0].set_title("Apple's log returns (2000-2022)")
    ax[1].plot(df_rv)
    ax[1].set_title("Annualized realized volatility")
    plt.show()
    plt.close()
