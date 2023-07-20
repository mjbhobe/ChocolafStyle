""" plot.py - plot stock prices using plotting libraries """
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8")
# print(plt.style.available)
# sys.exit(-1)

START_DATE, END_DATE = "2000-01-01", "2023-03-31"
SYMBOLS = ["AAPL"]

# download AAPL stock price
msft_df = yf.download(
    "MSFT",  # one stock or list of stock symbols ['AAPL','MSFT','AMZN']
    start=START_DATE,  # from date
    end=END_DATE,  # to date
    # auto_adjust=True,     # adjust OHLC automatically?
    # actions=True,         # download dividends & stock splits
    # interval="1d",        # Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo Intraday data cannot extend last 60 days
    progress=False,
)
msft_df.rename(columns={"Adj Close": "Adj_Close"}, inplace=True)
print(msft_df.tail())

# convert the price to returns
""" 
stock prices are usually non-stationary, which means that their means & variance change
over time. For any time-series analysis, stock data series must be stationary. Hence we
convert the stock prices to returns, which have constant mean & variance over time.
We have various types of returns
    Simple returns: aggregate over assets; simple returns of a portfolio is the weighted 
      sum of returns ofindividual assets in the portfolio. 
      It is calculated using formula below
            R[t] = (P[t] - P[t-1]) / P[t-1] = (P[t] / P[t-1]) - 1
    Log returns: aggregate over time & is calculated using formula below
            r[t] = log(P[t] / P[t-1]) = log(P[t]) - log(P[t-1])
    where P[t] is price of the asset at any time 't' - above formulae do not consider dividends!
Best practice when using stock prices is to use adjusted values, which take into
account variations due to stock-split, dividends etc. (also called Corporate Actions)
"""

# calculate the returns on Adj close price
df = msft_df.loc[:, ["Adj_Close"]]
# pandas has the formula for simple returns as below
df["Simple_Rtn"] = df.Adj_Close.pct_change()
df["Log_Rtn"] = np.log(df.Adj_Close / df.Adj_Close.shift(1))
print(df.head())

# plot the data using traditional Matplotlib calls
fig, ax = plt.subplots(3, 1, figsize=(24, 20), sharex=True)
df.Adj_Close.plot(ax=ax[0])
ax[0].set(title=f"MSFT time series: {START_DATE} - {END_DATE}", ylabel="Stock Price ($)")
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
df.iplot(subplots=True, shape=(3, 1), shared_xaxes=True, title=f"MSFT time series: {START_DATE} - {END_DATE}")
# nit_notebook_mode()
