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
    df = download_stock("RELIANCE.NS")
    macd = MACD(df, 12, 26, 9)
    macd_plot = [
        mpf.make_addplot(
            (macd["macd"]), color="#606060", panel=2, ylabel="MACD", secondary_y=False
        ),
        mpf.make_addplot((macd["signal"]), color="#1f77b4", panel=2, secondary_y=False),
        mpf.make_addplot((macd["bar_positive"]), type="bar", color="#4dc790", panel=2),
        mpf.make_addplot((macd["bar_negative"]), type="bar", color="#fd6b6c", panel=2),
    ]
    mpf.plot(
        df,
        type="candle",
        volume=True,
        addplot=macd_plot,
        figscale=1.5,
        panel_ratios=(4, 1, 3),
        style="yahoo",
    )
