#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NSE Buffett-Style Stock Screener (Growth + Dividend)
---------------------------------------------------
Requirements:
    pip install yfinance pandas numpy

Usage:
    1) Put your NSE symbols (with ".NS") into tickers.csv (header: symbol)
       A starter template is included.
    2) Run:
         python nse_buffett_screen.py
    3) The script will produce:
         - screen_output.csv  (all metrics + scores)
         - screen_top.csv     (top-ranked shortlist)
"""

import warnings
warnings.filterwarnings("ignore")

import os, sys
import math
import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf

# ------------------------------
# Config
# ------------------------------
TICKER_FILE = "tickers.csv"
OUT_ALL = "screen_output.csv"
OUT_TOP = "screen_top.csv"

# Scoring weights (tweak as you like)
WEIGHTS = {
    "roe": 2.0,                # Return on Equity
    "roce": 2.0,               # Return on Capital Employed / Invested
    "de_ratio": 1.5,           # Lower is better
    "interest_coverage": 1.0,  # Higher is better
    "fcf": 1.5,                # Positive & growing
    "div_yield": 1.5,          # 1% - 5% ideal band
    "eps_cagr": 2.0,           # >10% preferred
    "pe": 1.0                  # Lower relative PE better
}

MIN_YEARS = 4  # minimum years of annual statements we try to use for growth calcs

# ------------------------------
# Helper functions
# ------------------------------

def safe_div(a, b):
    try:
        if b is None or b == 0 or (isinstance(b, (int,float)) and abs(b) < 1e-12):
            return np.nan
        return a / b
    except Exception:
        return np.nan

def trailing_dividend_yield(ticker_obj, price):
    """Compute TTM dividend yield from dividends series."""
    try:
        dv = ticker_obj.dividends
        if dv is None or dv.empty or price is None or price <= 0:
            return np.nan
        one_year_ago = pd.Timestamp.today(tz=dv.index.tz) - pd.DateOffset(years=1)
        ttm = dv[dv.index >= one_year_ago].sum()
        return float(ttm) / float(price)
    except Exception:
        return np.nan

def latest_price(ticker_obj):
    try:
        finfo = {}
        try:
            finfo = ticker_obj.fast_info or {}
        except Exception:
            finfo = {}
        px = finfo.get("last_price")
        if px is None or (isinstance(px, float) and not math.isfinite(px)):
            # fallback to history
            hist = ticker_obj.history(period="5d", auto_adjust=False)
            if hist is not None and not hist.empty:
                px = float(hist["Close"].iloc[-1])
        return float(px) if px is not None else np.nan
    except Exception:
        return np.nan

def get_info_field(ticker_obj, field):
    try:
        info = ticker_obj.info or {}
        return info.get(field, np.nan)
    except Exception:
        return np.nan

def compute_roe(income_df, bal_df):
    """
    ROE ~ Net Income / Average Equity
    Uses last annual column. Equity from balance_sheet: 'Total Stockholder Equity'
    """
    try:
        ni = income_df.loc["Net Income"].dropna()
        eq = bal_df.loc["Total Stockholder Equity"].dropna()
        if ni.empty or eq.empty:
            return np.nan
        # last year
        ni_last = float(ni.iloc[0])
        # average equity (last 2 periods if available)
        if len(eq) >= 2:
            avg_eq = float((eq.iloc[0] + eq.iloc[1]) / 2.0)
        else:
            avg_eq = float(eq.iloc[0])
        return safe_div(ni_last, avg_eq)
    except Exception:
        return np.nan

def compute_roce(income_df, bal_df):
    """
    ROCE ~ EBIT / (Total Assets - Current Liabilities)
    Approximations due to data availability.
    """
    try:
        # EBIT might be 'Ebit' or we approximate with Operating Income
        if "Ebit" in income_df.index:
            ebit = income_df.loc["Ebit"].dropna()
        elif "Operating Income" in income_df.index:
            ebit = income_df.loc["Operating Income"].dropna()
        else:
            return np.nan

        ta = bal_df.loc["Total Assets"].dropna() if "Total Assets" in bal_df.index else None
        cl = bal_df.loc["Total Current Liabilities"].dropna() if "Total Current Liabilities" in bal_df.index else None
        if ebit is None or ebit.empty or ta is None or ta.empty or cl is None or cl.empty:
            return np.nan

        ebit_last = float(ebit.iloc[0])
        capital_employed = float(ta.iloc[0] - cl.iloc[0])
        return safe_div(ebit_last, capital_employed)
    except Exception:
        return np.nan

def compute_de_ratio(bal_df):
    """Debt to Equity = Total Debt / Total Equity"""
    try:
        # Debt: try Total Debt else Sum of ST + LT debt
        if "Total Debt" in bal_df.index:
            debt = bal_df.loc["Total Debt"].dropna()
        else:
            parts = []
            for k in ["Short Long Term Debt", "Long Term Debt", "Short Term Debt"]:
                if k in bal_df.index:
                    parts.append(bal_df.loc[k].dropna())
            if parts:
                debt = sum(p for p in parts if p is not None)
            else:
                return np.nan

        eq = bal_df.loc["Total Stockholder Equity"].dropna() if "Total Stockholder Equity" in bal_df.index else None
        if eq is None or eq.empty or debt is None or len(debt)==0:
            return np.nan
        return safe_div(float(debt.iloc[0]), float(eq.iloc[0]))
    except Exception:
        return np.nan

def compute_interest_coverage(income_df):
    """Interest Coverage = EBIT / Interest Expense"""
    try:
        if "Ebit" in income_df.index:
            ebit = float(income_df.loc["Ebit"].dropna().iloc[0])
        elif "Operating Income" in income_df.index:
            ebit = float(income_df.loc["Operating Income"].dropna().iloc[0])
        else:
            return np.nan

        if "Interest Expense" in income_df.index:
            ie = float(abs(income_df.loc["Interest Expense"].dropna().iloc[0]))
        else:
            return np.nan

        return safe_div(ebit, ie)
    except Exception:
        return np.nan

def compute_fcf(cash_df):
    """FCF = Operating Cash Flow - Capital Expenditure (last year)"""
    try:
        ocf = cash_df.loc["Total Cash From Operating Activities"].dropna() if "Total Cash From Operating Activities" in cash_df.index else None
        capex = cash_df.loc["Capital Expenditures"].dropna() if "Capital Expenditures" in cash_df.index else None
        if ocf is None or capex is None or ocf.empty or capex.empty:
            return np.nan
        return float(ocf.iloc[0]) - float(capex.iloc[0])
    except Exception:
        return np.nan

def compute_eps_cagr(income_df, info, years=5):
    """Approximate EPS CAGR using Net Income and current sharesOutstanding over N years."""
    try:
        if "Net Income" not in income_df.index:
            return np.nan
        ni_series = income_df.loc["Net Income"].dropna()
        if len(ni_series) < years + 1:
            return np.nan
        # Use current shares outstanding as proxy (crude but robust for screening)
        shares = info.get("sharesOutstanding", np.nan)
        if shares is None or not isinstance(shares, (int,float)) or shares <= 0:
            return np.nan
        eps_now = float(ni_series.iloc[0]) / float(shares)
        eps_past = float(ni_series.iloc[years]) / float(shares)
        if eps_past <= 0 or eps_now <= 0:
            return np.nan
        cagr = (eps_now / eps_past) ** (1.0/years) - 1.0
        return cagr
    except Exception:
        return np.nan

def percent(x):
    if pd.isna(x):
        return np.nan
    return 100.0 * float(x)

def score_row(row):
    """Weighted score based on thresholds; scale to 0-100."""
    score = 0.0
    weight_sum = sum(WEIGHTS.values())

    # ROE: >15% good, scale up to 30%+
    if not pd.isna(row["roe_pct"]):
        s = min(max((row["roe_pct"] - 10) / 20, 0), 1)  # 10%->0; 30%->1
        score += s * WEIGHTS["roe"]

    # ROCE: >15% good
    if not pd.isna(row["roce_pct"]):
        s = min(max((row["roce_pct"] - 10) / 20, 0), 1)
        score += s * WEIGHTS["roce"]

    # Debt/Equity: lower is better; 0 -> 1, 0.5 -> 0.5, 1.0 -> 0
    if not pd.isna(row["de_ratio"]):
        s = 1.0 - min(max(row["de_ratio"] / 1.0, 0), 1)  # D/E 0 =>1; D/E>=1 =>0
        score += s * WEIGHTS["de_ratio"]

    # Interest coverage: 1->0, 10->1 (cap at 10)
    if not pd.isna(row["interest_coverage"]):
        s = min(max((row["interest_coverage"] - 1) / 9.0, 0), 1)
        score += s * WEIGHTS["interest_coverage"]

    # FCF: positive -> 1, negative -> 0
    if not pd.isna(row["fcf"]):
        s = 1.0 if row["fcf"] > 0 else 0.0
        score += s * WEIGHTS["fcf"]

    # Dividend yield: ideal 1% - 5% (scale)
    if not pd.isna(row["div_yield_pct"]):
        y = row["div_yield_pct"]
        if y <= 0:
            s = 0.0
        elif 1 <= y <= 5:
            s = 1.0
        else:
            # if >5%, partial score (maybe unsustainably high)
            s = 0.5
        score += s * WEIGHTS["div_yield"]

    # EPS CAGR 5y: >10% good; 0->0, 10%->0.5, 20%->1
    if not pd.isna(row["eps_cagr_pct"]):
        s = min(max((row["eps_cagr_pct"]) / 20.0, 0), 1)  # 0..20% -> 0..1
        score += s * WEIGHTS["eps_cagr"]

    # PE: lower is better; PE 10->1, 40->0
    if not pd.isna(row["pe"]):
        pe = row["pe"]
        if pe <= 0 or np.isinf(pe):
            s = 0.0
        else:
            s = 1.0 - min(max((pe - 10) / 30.0, 0), 1)  # 10=>1; 40+=>0
        score += s * WEIGHTS["pe"]

    # normalize to 0-100
    return round(100.0 * score / weight_sum, 2)

def main():
    if not os.path.exists(TICKER_FILE):
        raise SystemExit(f"Ticker file not found: {TICKER_FILE}")

    symbols = pd.read_csv(TICKER_FILE)["symbol"].dropna().astype(str).str.strip().tolist()
    print(f"Loaded symbols: {symbols}")

    results = []

    for sym in symbols:
        try:
            print(f"Analysing symbol {sym}...")
            tkr = yf.Ticker(sym)
            price = latest_price(tkr)
            info = tkr.info or {}

            # Fundamentals (annual)
            income = tkr.income_stmt
            bal = tkr.balance_sheet
            cash = tkr.cashflow

            if isinstance(income, pd.DataFrame):
                income = income.copy()
            else:
                income = pd.DataFrame()

            if isinstance(bal, pd.DataFrame):
                bal = bal.copy()
            else:
                bal = pd.DataFrame()

            if isinstance(cash, pd.DataFrame):
                cash = cash.copy()
            else:
                cash = pd.DataFrame()

            # compute metrics
            roe = compute_roe(income, bal)
            roce = compute_roce(income, bal)
            de = compute_de_ratio(bal)
            ic = compute_interest_coverage(income)
            fcf = compute_fcf(cash)
            dy = trailing_dividend_yield(tkr, price)

            # PE (trailing)
            pe = np.nan
            try:
                fi = tkr.fast_info or {}
                pe = fi.get("trailing_pe", np.nan)
                if (pe is None) or (isinstance(pe, float) and not math.isfinite(pe)):
                    pe = info.get("trailingPE", np.nan)
            except Exception:
                pe = info.get("trailingPE", np.nan)

            eps_cagr = compute_eps_cagr(income, info, years=5)

            row = {
                "symbol": sym,
                "price": price,
                "roe_pct": percent(roe),
                "roce_pct": percent(roce),
                "de_ratio": de if (de is None or np.isnan(de)) else float(de),
                "interest_coverage": ic if (ic is None or np.isnan(ic)) else float(ic),
                "fcf": np.nan if fcf is None else float(fcf),
                "div_yield_pct": percent(dy) if not pd.isna(dy) else np.nan,
                "pe": np.nan if pe is None else float(pe),
                "eps_cagr_pct": percent(eps_cagr) if not pd.isna(eps_cagr) else np.nan,
            }
            results.append(row)

        except Exception as e:
            results.append({
                "symbol": sym,
                "error": str(e)
            })

    df = pd.DataFrame(results)

    # Compute composite score
    df["score"] = df.apply(score_row, axis=1)

    # Sort
    df_sorted = df.sort_values(["score", "div_yield_pct", "roe_pct"], ascending=[False, False, False])

    # Write outputs
    df_sorted.to_csv(OUT_ALL, index=False)

    # shortlist top N that pass some sanity thresholds
    top = df_sorted.copy()
    # Example filters (adjust to taste)
    top = top[
        (top["roe_pct"] >= 15) &
        (top["roce_pct"] >= 12) &
        (top["de_ratio"] <= 0.8) &
        (top["div_yield_pct"] >= 0.5)  # at least some yield
    ]
    top = top.sort_values("score", ascending=False).head(15)
    top.to_csv(OUT_TOP, index=False)

    print(f"\nSaved: {OUT_ALL} (all results)")
    print(f"Saved: {OUT_TOP} (shortlist)")
    print("\nTip: Open the CSVs in Excel for easy filtering/sorting.")
    print("\nDone.")

if __name__ == "__main__":
    main()
