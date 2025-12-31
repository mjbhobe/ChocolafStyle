import streamlit as st
import yfinance as yf
from fin_charting import create_financial_chart

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Finance Dashboard")

# Custom CSS for better spacing
st.markdown("""
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 0rem; }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 2. Initialize Session State
if "show_chart" not in st.session_state:
    st.session_state.show_chart = False
if "data_cache" not in st.session_state:
    st.session_state.data_cache = None
if "company_name" not in st.session_state:
    st.session_state.company_name = ""

# 3. Data Fetching Function (Cached)
@st.cache_data(ttl=3600)
def fetch_data(symbol):
    """
    Downloads 10 years of data for all three intervals.
    multi_level_index=False is used to prevent the 'Missing Candlestick' bug.
    """
    try:
        ticker_obj = yf.Ticker(symbol)
        # Try to get the long name, fallback to ticker symbol
        name = ticker_obj.info.get('longName', symbol)
        
        intervals = {"Daily": "1d", "Weekly": "1wk", "Monthly": "1mo"}
        data = {}
        
        for label, code in intervals.items():
            df = yf.download(
                symbol, 
                period="10y", 
                interval=code, 
                multi_level_index=False
            )
            if df.empty:
                return None, None
            data[label] = df
            
        return data, name
    except Exception as e:
        return None, str(e)

# 4. Sidebar UI
with st.sidebar:
    st.header("Search Settings")
    ticker_input = st.text_input("Enter Stock Symbol", value="PIDILITIND.NS").upper()
    interval_choice = st.radio("Select Interval", ["Daily", "Weekly", "Monthly"])
    
    # Action Button
    if st.button("Plot Chart", use_container_width=True):
        with st.spinner(f"Downloading data for {ticker_input}..."):
            data, name = fetch_data(ticker_input)
            
            if data:
                st.session_state.data_cache = data
                st.session_state.company_name = name
                st.session_state.show_chart = True
                st.session_state.current_ticker = ticker_input
            else:
                st.error(f"Could not find/download data for {ticker_input}. Please check the ticker symbol.")
                st.session_state.show_chart = False

# 5. Main Area Logic
if not st.session_state.show_chart:
    # Initial landing message
    st.info('Please enter stock symbol, select interval & click "Plot Chart" to display financial chart.')
else:
    # Retrieve the specific interval from our session-stored data
    df_to_plot = st.session_state.data_cache.get(interval_choice)
    
    if df_to_plot is not None and not df_to_plot.empty:
        # Call the external plotting module
        fig = create_financial_chart(
            df_to_plot, 
            st.session_state.current_ticker, 
            st.session_state.company_name, 
            interval_choice
        )
        
        # Display the plot
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("No data available to plot.")