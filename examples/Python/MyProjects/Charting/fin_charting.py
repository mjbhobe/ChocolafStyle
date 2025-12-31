"""
financial_plot.py - plots a financial chart much like TradingView

@Author: Manish Bhobe
My experiments with Python for Finance. Code shared for learning purposed only!
"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_financial_chart(df, ticker_symbol, company_name, interval_label):
    # CRITICAL FIX: Flatten MultiIndex columns from yfinance
    # This converts ('Close', 'AAPL') into just 'Close'
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Indicator Calculations
    df['EMA5'] = df['Close'].ewm(span=5, adjust=False).mean()
    df['EMA13'] = df['Close'].ewm(span=13, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
    df['EMA200'] = df['Close'].ewm(span=200, adjust=False).mean()
    
    sma20 = df['Close'].rolling(window=20).mean()
    std20 = df['Close'].rolling(window=20).std()
    df['BB_Upper'] = sma20 + (std20 * 2)
    df['BB_Lower'] = sma20 - (std20 * 2)
    df['BB_Mid'] = sma20

    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])

    # 1. Bollinger Bands
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], line=dict(color='#2962FF', width=1), showlegend=False, hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], line=dict(color='#2962FF', width=1), fill='tonexty', fillcolor='rgba(41, 98, 255, 0.07)', showlegend=False, hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_Mid'], line=dict(color='#F23645', width=1.5), name='BB Median'))

    # 2. Volume Bars
    vol_colors = ['rgba(8, 153, 129, 0.6)' if c >= o else 'rgba(242, 54, 69, 0.6)' for c, o in zip(df['Close'], df['Open'])]
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=vol_colors, name='Volume', hovertemplate="Vol: %{y:,.0f}<extra></extra>"), secondary_y=True)

    # 3. Candlesticks
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        increasing_line_color='#089981', decreasing_line_color='#F23645',
        increasing_fillcolor='#089981', decreasing_fillcolor='#F23645',
        name='OHLC',
        hovertemplate="O: %{open:.2f}<br>H: %{high:.2f}<br>L: %{low:.2f}<br>C: %{close:.2f}<extra></extra>"
    ))

    # 4. EMA Lines
    ema_map = [('EMA5', '#2962FF', 2), ('EMA13', '#22AB94', 2), ('EMA26', '#848E9C', 2), ('EMA50', '#E91E63', 4), ('EMA200', '#9C27B0', 4)]
    for col, color, width in ema_map:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], line=dict(color=color, width=width), name=col, hovertemplate=f"{col}: %{{y:.2f}}<extra></extra>"))

    fig.update_layout(
        template="plotly_white",
        height=750,
        hovermode="x unified",
        title=f"<b>{company_name} ({ticker_symbol})</b> - {interval_label}",
        # MINIMAL SCROLLER: Reduced thickness and padding
        xaxis=dict(
            rangeslider=dict(visible=True, thickness=0.04), 
            range=[df.index[-100], df.index[-1]], 
            type='date'
        ),
        yaxis=dict(side="right", autorange=True, fixedrange=False),
        yaxis2=dict(visible=False, range=[0, df['Volume'].max() * 4]),
        margin=dict(l=40, r=40, t=80, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig