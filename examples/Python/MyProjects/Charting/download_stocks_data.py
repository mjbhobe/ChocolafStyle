"""
download_stocks_data.py - downloads stocks data listed in holdings_mjb.csv
file and calculates quarterly performance of each stock

@author: Manish Bhobe
My experiments with Python & Finance. Code shared for learning purposed only!
"""
import sys
from pathlib import Path
import yfinance as yf
import pandas as pd
from datetime import datetime
from rich.console import Console

DATA_FILE_PATH = Path(__file__).parent / "holdings_mjb.csv"
console = Console()


def get_quarterly_performance_report_(csv_file):
    # 1. Load tickers and quantities from CSV
    portfolio_df = pd.read_csv(csv_file)
    # Strip whitespace just in case the CSV has spaces after commas
    portfolio_df.columns = portfolio_df.columns.str.strip()
    portfolio_df['SYMBOL'] = portfolio_df['SYMBOL'].str.strip()

    tickers = portfolio_df['SYMBOL'].tolist()
    qtys = portfolio_df.set_index('SYMBOL')['NUM_SHARES']

    # 2. Download 5 years of Adjusted Close data
    # We download slightly more than 5y to ensure we catch the very first day
    raw_data = yf.download(tickers, period="5y", auto_adjust=True)

    # Extract only the Close prices (MultiIndex handling)
    if len(tickers) > 1:
        prices = raw_data['Close']
    else:
        # If only one ticker, yfinance returns a Series or simple DF
        prices = raw_data['Close'].to_frame(name=tickers[0])

    # 3. Get the "First Day" price (5 years ago)
    first_day_price = prices.iloc[0]

    # 4. Get prices at the end of each calendar quarter
    # 'QE' stands for Quarter End (formerly 'Q')
    quarterly_prices = prices.resample('QE').last()

    # 5. Build the Final Report DataFrame
    # Transpose quarterly_prices so SYMBOLs are rows and dates are columns
    report = quarterly_prices.T

    # Rename columns to dd-Mmm-yy format
    report.columns = [col.strftime('%d-%b-%y') for col in report.columns]

    # Insert the 'qty' and 'Start Price' at the beginning
    report.insert(0, 'NUM_SHARES', qtys)
    report.insert(1, 'Start Price (' + prices.index[0].strftime('%d-%b-%y') + ')', first_day_price)

    return report


def get_quarterly_performance_report(csv_file):
    # 1. Load tickers and quantities from CSV
    portfolio_df = pd.read_csv(csv_file)
    portfolio_df.columns = portfolio_df.columns.str.strip()
    portfolio_df['SYMBOL'] = portfolio_df['SYMBOL'].str.strip()

    tickers = portfolio_df['SYMBOL'].tolist()
    qtys = portfolio_df.set_index('SYMBOL')['NUM_SHARES']

    # 2. Download 5 years of Adjusted Close data
    raw_data = yf.download(tickers, period="5y", auto_adjust=True)

    # Extract Close prices
    if len(tickers) > 1:
        prices = raw_data['Close']
    else:
        prices = raw_data['Close'].to_frame(name=tickers[0])

    # 3. Resample to get Quarter End prices
    # 'QE' captures the last trading day of each calendar quarter
    quarterly_prices = prices.resample('QE').last()

    # 4. Build the report by interweaving Price and Value columns
    # We start with the 'qty' column as the base
    report = pd.DataFrame(index=tickers)
    report['NUM_SHARES'] = qtys

    # Iterate through each date in the quarterly data
    for date in quarterly_prices.index:
        date_str = date.strftime('%d-%b-%y')
        price_col = f"Close_{date_str}"
        value_col = f"Value_{date_str}"

        # Get prices for this specific date for all tickers
        current_prices = quarterly_prices.loc[date]

        # Add the Price column
        report[price_col] = current_prices

        # Add the Value column (Price * Qty)
        report[value_col] = report[price_col] * report['NUM_SHARES']

    # add a row at the bottom that shows totals of all the "Value_XXX" cols
    # Create a totals row with the same columns as the report
    totals_row = pd.Series(name='TOTALS', dtype=object)
    totals_row['NUM_SHARES'] = None  # Leave qty blank for the totals row

    # Loop through columns to sum only those starting with 'Value_'
    for col in report.columns:
        if col.startswith('Value_'):
            totals_row[col] = report[col].sum()
        # elif col != 'NUM_SHARES':
        #     totals_row[col] = None  # Leave everything else blank

    # Append the totals row to the dataframe
    report = pd.concat([report, totals_row.to_frame().T])

    return report


# --- Execution ---
if __name__ == "__main__":
    try:
        # if not DATA_FILE_PATH.exists():
        #     raise FileNotFoundError

        final_report = get_quarterly_performance_report(str(DATA_FILE_PATH))

        # Display the result
        print("Quarterly Performance Report (Prices per Share):")
        print(final_report.to_string())

        # Example: Access specific stock performance
        # print(final_report.loc["AAPL"])

    except FileNotFoundError:
        console.print(f"[red]Error: \'{DATA_FILE_PATH.name}\' not found in the current directory.[/red]")
    except Exception as e:
        console.print(f"[red]An error occurred: {e}[/red]")
