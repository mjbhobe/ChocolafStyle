#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import mplfinance as mpf

START_DATE, END_DATE = "2023-04-01", "2024-01-12"


def download_stock(symbol, start_date=START_DATE, end_date=END_DATE) -> pd.DataFrame:
    df = yf.download(symbol, start=start_date, end=end_date, progress=False)
    # df = df.reset_index()
    return df


def BollingerBands(df, window=20, no_of_std=2):
    bbands = pd.DataFrame()
    bbands["rolling_mean"] = df["Close"].rolling(window).mean()
    bbands["rolling_std"] = df["Close"].rolling(window).std()
    bbands["rolling_volume"] = df["Volume"].rolling(window).mean()
    bbands["bband_high"] = bbands["rolling_mean"] + (bbands["rolling_std"] * no_of_std)
    bbands["bband_low"] = bbands["rolling_mean"] - (bbands["rolling_std"] * no_of_std)
    return bbands


def MACD(df, window_slow, window_fast, window_signal):
    macd = pd.DataFrame()
    macd["ema_slow"] = df["Close"].ewm(span=window_slow).mean()
    macd["ema_fast"] = df["Close"].ewm(span=window_fast).mean()
    macd["macd"] = macd["ema_slow"] - macd["ema_fast"]
    macd["signal"] = macd["macd"].ewm(span=window_signal).mean()
    macd["diff"] = macd["macd"] - macd["signal"]
    macd["bar_positive"] = macd["diff"].map(lambda x: x if x > 0 else 0)
    macd["bar_negative"] = macd["diff"].map(lambda x: x if x < 0 else 0)
    return macd


if __name__ == "__main__":
    green_color = "#089981"
    red_color = "#F23645"
    blue_color = "#2962ff"
    bband_limits_color = "#1c6ba3"
    bband_fill_color = "#eff7fe"
    bband_mean_color = "#000000"

    df = download_stock("RELIANCE.NS")

    bbands = BollingerBands(df, 20, 2)
    macd = MACD(df, 12, 26, 9)

    indicator_plots = [
        # for make_addplot additional keywords, see _valid_addplot_kwargs()
        # on page https://github.com/matplotlib/mplfinance/blob/master/src/mplfinance/plotting.py
        mpf.make_addplot(
            bbands[["bband_high", "bband_low"]],
            color=bband_limits_color,
            linewidths=2,
            panel=0,
        ),
        mpf.make_addplot(bbands["rolling_mean"], color=bband_mean_color, panel=0),
        mpf.make_addplot(
            (macd["macd"]), color=blue_color, panel=2, ylabel="MACD", secondary_y=False
        ),
        mpf.make_addplot((macd["signal"]), color=red_color, panel=2, secondary_y=False),
        mpf.make_addplot(
            (macd["bar_positive"]), type="bar", width=1, color=green_color, panel=2
        ),
        mpf.make_addplot(
            (macd["bar_negative"]), type="bar", width=1, color=red_color, panel=2
        ),
    ]
    fig, ax = mpf.plot(
        df,
        type="candle",
        volume=True,
        addplot=indicator_plots,
        figscale=1.5,
        panel_ratios=(4, 1, 3),
        style="yahoo",
        returnfig=True,
    )
    # now draw fill between bollinger bands
