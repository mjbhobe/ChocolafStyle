""" stylized_facts.py: get facts about an index """
import sys
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as scs
import statsmodels.api as sm
import statsmodels.tsa.api as smt
from download import download_stock_prices

# print(plt.style.available)
# sys.exit(-1)

START_DATE, END_DATE = "1985-01-01", "2023-11-30"

if __name__ == "__main__":
    df = download_stock_prices("MSFT", START_DATE, END_DATE)
    print(df.head())
    # generate 1000 numbers between min & max of log returns
    r_range = np.linspace(np.min(df.Log_Rtn), np.max(df.Log_Rtn), num=1000)
    # calculate mean & std-deviation of Log_Rtn
    mu, sigma = df.Log_Rtn.mean(), df.Log_Rtn.std()
    # generate normal distribution for 1000 linspace numbers with mean = mu & std= sigma
    norm_pdf = scs.norm.pdf(r_range, loc=mu, scale=sigma)
    # plot histogram & QQ-plot
    fig, ax = plt.subplots(1, 2, figsize=(16, 8))
    # histogram with norm distribution
    sns.distplot(df.Log_Rtn, kde=False, norm_hist=True, ax=ax[0])
    ax[0].set_title("Distribution of MSFT Returns", fontsize=12)
    ax[0].plot(
        r_range, norm_pdf, color="firebrick", lw=2, label=f"N({mu:.2f}, {sigma**2:.4f})"
    )
    ax[0].legend(loc="upper left")
    # QQ-plot
    qq = sm.qqplot(df.Log_Rtn.values, line="s", ax=ax[1])
    ax[1].set_title("Q-Q plot", fontsize=12)
    plt.show()
