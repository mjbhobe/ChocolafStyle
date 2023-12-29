""" download.py - download stock prices using yfinance """
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

# print(plt.style.available)
# sys.exit(-1)

START_DATE, END_DATE = "1990-01-01", "2023-12-11"


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
        # auto_adjust=True,     # adjust OHLC automatically?
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


def adjust_prices_for_inflation(
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
    quandl.ApiConfig.api_key = config["config_keys"]["quandl.ApiConfig.api_key"]

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
    plt.style.use("seaborn-v0_8")
    df = download_stock_prices("RELIANCE.NS", START_DATE, END_DATE)
    print(df.tail())
    df2 = adjust_prices_for_inflation(df, START_DATE, END_DATE)

    plt.figure(figsize=(10, 6))
    plt.plot(df2["Simple_Rtn"], lw=2, label="Simple Returns")
    plt.plot(df2["Inflation_Rate"], lw=2, label="Inflation Rate")
    plt.plot(df2["Real_Rtn"], lw=2, label="Real Returns")
    plt.title("AAPL Stock Returns")
    plt.legend()
    plt.show()
