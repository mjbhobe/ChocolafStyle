""" detect_outliers.py - detect outliers in stock price data & returns """
import sys
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from download import download_stock_prices

# print(plt.style.available)
# sys.exit(-1)

START_DATE, END_DATE = '2000-01-01', '2023-03-31'


def detect_outliers(row, n_sigmas = 3):
    x = row['Simple_Rtn']
    mu = row['mean']
    sigma = row['std']

    if (x > mu + n_sigmas * sigma) or (x < mu - n_sigmas * sigma):
        return 1
    else:
        return 0


if __name__ == "__main__":
    # plt.style.use('seaborn')
    stocks = {
        'AAPL': 'Apple', 'MSFT': 'Microsoft', 'AMZN': 'Amazon', 'GOOG': 'Alphabet'
    }  # , 'AMZN': 'Amazon', 'META': 'Meta'}
    dataframes = []
    for symbol, stock in stocks.items():
        print(f"Downloading {symbol} prices", flush = True)
        df = download_stock_prices(symbol, START_DATE, END_DATE)
        # print(df.tail())
        df_rolling = df[['Simple_Rtn']].rolling(window = 21).agg(['mean', 'std'])
        df_rolling.columns = df_rolling.columns.droplevel()

        df = df.join(df_rolling)
        # print(df.tail())

        # detect outliers using 3 sigma method
        df['outlier'] = df.apply(detect_outliers, axis = 1)
        # select Simple returns column for all outlier rows
        df_outliers = df.loc[df['outlier'] == 1, ['Simple_Rtn']]
        dataframes.append((df, df_outliers, stock))

    # now display the plots
    fig, ax = plt.subplots(len(dataframes), figsize = (20, 8), sharex = True)
    for i, (df, df_outliers, stock) in enumerate(dataframes):
        ax[i].plot(df.index, df.Simple_Rtn, color = 'SteelBlue', label = 'Normal')
        ax[i].scatter(
            df_outliers.index, df_outliers.Simple_Rtn, color = 'firebrick', label = "Anamoly"
        )
        ax[i].set_title(f"{stock}'s Stock Returns")
        ax[i].legend(loc = "best")
    plt.show()
