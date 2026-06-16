"""analyze_nifty50_stocks.py: iterate over all stocks that are part of Nifty 50
   index and analyze if they are a good potential for long term investment.

Author: Manish Bhobé
My experiments with Python, AI and Generative AI
Code shared for learning purposes only!
"""

import os
import yfinance as yf
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

# load API keys from .env file
load_dotenv(override=True)

# create instance of LLM
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# NIFTY 50 stock symbols (as per NSE as of Juen 2026)
nifty50_symbols = [
    "ADANIENT.NS",
    "ADANIPORTS.NS",
    "APOLLOHOSP.NS",
    "ASIANPAINT.NS",
    "AXISBANK.NS",
    "BAJAJ-AUTO.NS",
    "BAJAJFINSV.NS",
    "BAJFINANCE.NS",
    "BEL.NS",
    "BHARTIARTL.NS",
    "BPCL.NS",
    "BRITANNIA.NS",
    "CIPLA.NS",
    "COALINDIA.NS",
    "DIVISLAB.NS",
    "DRREDDY.NS",
    "EICHERMOT.NS",
    "GRASIM.NS",
    "HCLTECH.NS",
    "HDFCBANK.NS",
    "HDFCLIFE.NS",
    "HEROMOTOCO.NS",
    "HINDALCO.NS",
    "HINDUNILVR.NS",
    "ICICIBANK.NS",
    "INDUSINDBK.NS",
    "INFY.NS",
    "ITC.NS",
    "JSWSTEEL.NS",
    "KOTAKBANK.NS",
    "LT.NS",
    "LTM.NS",  # LTI Mindtree - On Yahoo Finance its LTM.NS but on NSE its LTIM.NS
    "M&M.NS",
    "MARUTI.NS",
    "NESTLEIND.NS",
    "NTPC.NS",
    "ONGC.NS",
    "POWERGRID.NS",
    "RELIANCE.NS",
    "SBILIFE.NS",
    "SBIN.NS",
    "SUNPHARMA.NS",
    "TATACONSUM.NS",
    "TMCV.NS",  # new symbol for TATA Motors
    "TATASTEEL.NS",
    "TCS.NS",
    "TECHM.NS",
    "TITAN.NS",
    "ULTRACEMCO.NS",
    "WIPRO.NS",
]


# Function to fetch stock data and calculate key metrics
def get_stock_fundamentals(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        # Extract Key Metrics
        data = {
            "Symbol": symbol,
            "Company": info.get("longName", "N/A"),
            "Market Cap (Cr)": info.get("marketCap", 0) / 1e7,  # Convert to Crore
            "P/E Ratio": info.get("trailingPE", np.nan),
            "P/B Ratio": info.get("priceToBook", np.nan),
            "ROE (%)": (
                info.get("returnOnEquity", 0) * 100
                if info.get("returnOnEquity")
                else np.nan
            ),
            "ROCE (%)": (
                info.get("returnOnAssets", 0) * 100
                if info.get("returnOnAssets")
                else np.nan
            ),  # Proxy for ROCE
            "Debt/Equity": info.get("debtToEquity", np.nan),
            "Profit Margin (%)": (
                info.get("profitMargins", 0) * 100
                if info.get("profitMargins")
                else np.nan
            ),
            "Revenue Growth (YoY %)": (
                info.get("revenueGrowth", 0) * 100
                if info.get("revenueGrowth")
                else np.nan
            ),
            "FCF (Cr)": (
                info.get("freeCashflow", 0) / 1e7
                if info.get("freeCashflow")
                else np.nan
            ),  # Convert to Crore
            "Dividend Yield (%)": (
                info.get("dividendYield", 0) * 100
                if info.get("dividendYield")
                else np.nan
            ),
            "EV/EBITDA": info.get("enterpriseToEbitda", np.nan),
        }
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None


# Fetch Data for all NIFTY 50 stocks
stocks_data = [get_stock_fundamentals(symbol) for symbol in nifty50_symbols]
stocks_df = pd.DataFrame([stock for stock in stocks_data if stock])


# Filter out NaN values
stocks_df.dropna(inplace=True)


# Define thresholds for selection
def evaluate_stock(stock):
    if (
        stock["P/E Ratio"] < 20
        and stock["P/B Ratio"] < 3
        and stock["ROE (%)"] > 15
        and stock["ROCE (%)"] > 12
        and stock["Debt/Equity"] < 1
        and stock["Profit Margin (%)"] > 10
        and stock["Revenue Growth (YoY %)"] > 10
        and stock["FCF (Cr)"] > 0
        and stock["EV/EBITDA"] < 12
    ):
        return "✅ Strong Buy"
    elif stock["P/E Ratio"] < 25 and stock["ROE (%)"] > 12:
        return "🔎 Moderate Buy"
    else:
        return "❌ Avoid"


# Apply evaluation criteria
stocks_df["Investment Recommendation"] = stocks_df.apply(evaluate_stock, axis=1)
print(stocks_df)


# Use OpenAI to generate recommendations
def get_openai_recommendation(stock):

    print(f"OpenAI analyzing stock {stock['Symbol']}")

    prompt = f"""
    Analyze the following stock based on key fundamental metrics and determine if it is 
    a good long-term investment:

    Company: {stock['Company']}
    Market Cap: {stock['Market Cap (Cr)']} Cr
    P/E Ratio: {stock['P/E Ratio']}
    P/B Ratio: {stock['P/B Ratio']}
    ROE: {stock['ROE (%)']}%
    ROCE: {stock['ROCE (%)']}%
    Debt-to-Equity: {stock['Debt/Equity']}
    Profit Margin: {stock['Profit Margin (%)']}%
    Revenue Growth: {stock['Revenue Growth (YoY %)']}%
    Free Cash Flow: {stock['FCF (Cr)']} Cr
    Dividend Yield: {stock['Dividend Yield (%)']}%
    EV/EBITDA: {stock['EV/EBITDA']}

    Based on these factors, provide a a> short/quick recommendation AND b> a detailed investment analysis and recommendation in proper markdown format, stating whether it is a **buy, hold, or avoid**, explaining the reasons in an investor-friendly language.

    Return response as a JSON object with the following structure:
    {{
        "symbol": the stock symbol,
        "short_recommendation": <<your short/quick recommendation>>,
        "detailed_analysis": <<your detailed investment analysis and recommendation in markdown format>>
    }}
    """

    response = openai.chat.completions.create(
        model="gpt-5-nano",
        # temperature=0.0,
        messages=[
            {"role": "system", "content": "You are a financial investment expert."},
            {"role": "user", "content": prompt},
        ],
    )

    response = response.choices[0].message.content.strip()
    print(f"OpenAI recommendation for {stock['Symbol']}:\n {response}")
    return response


# Generate AI Recommendations for Top 5 stocks
top_stocks = stocks_df[stocks_df["Investment Recommendation"] == "✅ Strong Buy"].head(
    5
)

# for testing
top_stocks = stocks_df.head(2)

if len(top_stocks) == 0:
    print("No strong buy stocks found based on the criteria.")
else:
    ai_recommendations = []
    for _, stock in top_stocks.iterrows():
        recommendation = get_openai_recommendation(stock)
        ai_recommendations.append(
            {"Company": stock["Company"], "AI Recommendation": recommendation}
        )

    # Convert to DataFrame and Display
    ai_recommendations_df = pd.DataFrame(ai_recommendations)
    print(ai_recommendations_df)
