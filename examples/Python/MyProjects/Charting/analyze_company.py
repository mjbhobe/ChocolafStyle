import yfinance as yf
import pandas as pd
import numpy as np
from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv

# load env variables from .env file
_ = load_dotenv(find_dotenv())

SYS_PROMPT = f"""
You are an expert at Finance, Financial Markets and Financial market ratio calculations and 
analysis of companies and can give expert and detailed recommendations.
"""
openai_client = OpenAI()


# Function to fetch data
def fetch_data(symbol):
    ticker = yf.Ticker(symbol)
    financials = ticker.financials.transpose()
    balance_sheet = ticker.balance_sheet.transpose()
    cash_flow = ticker.cashflow.transpose()

    return ticker, financials, balance_sheet, cash_flow


def get_peer_companies(ticker):
    # Create the prompt to retrieve the peer companies
    peer_cos_prompt = f"""
    I want to retrieve the top 5 peer companies of {ticker.info['symbol']} on the NSE (National Stock Exchange of India) that operate in the {ticker.info['industryDisp']} industry.
    Please provide your response in the form of a Python dictionary with the key being the NSE symbol of the company and the value 
    being the full name of the company. 
    Return the response as a string formatted as a Python dict with no surrounding text or markdown.
    """

    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYS_PROMPT},
            {
                "role": "user",
                "content": peer_cos_prompt,
            },
        ],
        temperature=0,
    )

    # # Use OpenAI API to complete the prompt
    # response = openai.Completion.create(
    #     engine="gpt-4",  # Use the GPT-4 engine for better responses
    #     prompt=prompt,
    #     max_tokens=200,
    #     temperature=0.2,
    # )

    # Extract the response
    # peers = response.choices[0].text.strip()
    peers = completion.choices[0].message.content
    print(f"Peers: {peers}")

    # Convert the response to a Python dict
    try:
        peer_dict = eval(peers)
    except Exception as e:
        peer_dict = {"error": str(e)}

    return peer_dict


# Function to calculate financial ratios
def calculate_ratios(financials, balance_sheet, cash_flow):
    ratios = {}

    # Revenue Growth
    ratios["Revenue Growth"] = financials["Total Revenue"].pct_change()

    # Net Profit Margin
    ratios["Net Profit Margin"] = financials["Net Income"] / financials["Total Revenue"]

    # EPS
    ratios["EPS"] = financials["Net Income"] / balance_sheet["Common Stock"]

    # ROE
    ratios["ROE"] = (
        financials["Net Income"] / balance_sheet["Stockholders Equity"]
    )  # balance_sheet["Total Stockholder Equity"]

    # Debt to Equity
    ratios["D/E"] = (
        balance_sheet["Current Liabilities"]
        / balance_sheet["Stockholders Equity"]
        # balance_sheet["Total Liab"] / balance_sheet["Total Stockholder Equity"]
    )

    # Free Cash Flow
    ratios["Free Cash Flow"] = (
        cash_flow["Free Cash Flow"]
        - cash_flow["Capital Expenditure"]
        # cash_flow["Total Cash From Operating Activities"]
        # - cash_flow["Capital Expenditures"]
    )

    return pd.DataFrame(ratios)


# Function to compare with peers
def compare_with_peers(symbol, peers):
    peer_ratios = {}

    for peer in peers:
        _, financials, balance_sheet, cash_flow = fetch_data(peer)
        peer_ratios[peer] = calculate_ratios(
            financials, balance_sheet, cash_flow
        ).mean()

    # Convert to DataFrame
    return pd.DataFrame(peer_ratios)


# Function to get recommendation using OpenAI API
def get_recommendation(symbol, report, peers=None):
    # Set your OpenAI API key in the environment variables
    reco_prompt = (
        f"Given the following financial performance report:\n\n{report}\n\n "
        f"First, give a commentary and your analysis of {symbol} performance\n"
    )
    if peers is not None:
        reco_prompt += f"Next, give a commentary and your analysis of how {symbol} has fares viz-a-viz peers {peers}\n"

    reco_prompt += f"Finally, What is your recommendation on this company's long-term investment potential?"

    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYS_PROMPT},
            {
                "role": "user",
                "content": reco_prompt,
            },
        ],
        temperature=0,
    )

    # response = openai.Completion.create(model="gpt-4", prompt=prompt, max_tokens=200)

    # return response.choices[0].text.strip()
    return completion.choices[0].message.content


# Main application
def main():
    st.title("Financial Analysis of Company")

    # Input company symbol
    symbol = st.text_input("Enter the Company Symbol:")

    # if symbol:
    #     # Example usage
    #     peer_companies = get_peer_companies(symbol)
    #     st.write(peer_companies)
    #     print(peer_companies)

    # Input peers
    # peers = st.text_input("Enter Peer Company Symbols (comma-separated):").split(",")

    if symbol:
        ticker, financials, balance_sheet, cash_flow = fetch_data(symbol)

        st.markdown(f"#### Basic Info for {symbol}")
        st.markdown(f"**Company Name:** {ticker.info['longName']}")
        st.markdown(f"**Business Summary:**")
        st.markdown(f"{ticker.info['longBusinessSummary']}")

        peers = get_peer_companies(ticker)
        st.markdown(f"**Peers (top {len(peers)})**")
        # st.markdown(f"```python\n{peers}\n```")
        for sym, descr in peers.items():
            st.markdown(f"- {descr} ({sym})")

        st.markdown(f"#### Financials")
        st.dataframe(financials)
        st.markdown(f"#### Balance Sheet")
        st.dataframe(balance_sheet)
        st.markdown(f"#### Cash Flows")
        st.dataframe(cash_flow)

        ratios = calculate_ratios(financials, balance_sheet, cash_flow)

        st.markdown(f"### Financial Ratios for {symbol}")
        st.dataframe(ratios)

        if peers:
            peer_comparison = compare_with_peers(symbol, peers)
            # add mean ratios of company to this dataframe
            peer_comparison[symbol] = ratios.mean().T

            st.markdown("### Peer Comparison")
            st.dataframe(peer_comparison)

        # # Generate report
        # report = f"Financial ratios for {symbol}:\n\n{ratios.to_markdown()}\n\n"
        # if peers:
        #     report += f"Peer comparison:\n\n{peer_comparison.to_markdown()}"
        # recommendation = get_recommendation(symbol, report, peers)

        # # Display recommendation
        # st.markdown("### AI Recommendation")
        # st.write(recommendation)

        # # Save report to file
        # with open(f"{symbol}_financial_report.md", "w") as file:
        #     file.write(f"# Financial Report for {symbol}\n\n")
        #     file.write(report)
        #     file.write(f"\n\n## AI Recommendation:\n{recommendation}")


if __name__ == "__main__":
    main()
