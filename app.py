import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(page_title="Gold (XAU/USD) AI Analyzer", layout="wide")
st.title("🏆 Gold (XAU/USD) Market Pattern Analyzer")
st.write("Real-time technical pattern and market structure scanner for Gold.")

# Sidebar Settings
st.sidebar.header("Chart Settings")
period = st.sidebar.selectbox("Select Time Period", ["1mo", "3mo", "6mo", "1y"], index=0)
interval = st.sidebar.selectbox("Select Candle Interval", ["15m", "30m", "1h", "1d"], index=2)

@st.cache_data(ttl=300)
def fetch_gold_data(p, i):
    data = yf.download("GC=F", period=p, interval=i)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    return data

# Fetch Data
with st.spinner("Downloading Gold Market Data..."):
    df = fetch_gold_data(period, interval)

if not df.empty:
    latest_price = float(df['Close'].iloc[-1])
    prev_price = float(df['Close'].iloc[-2])
    change = latest_price - prev_price

    # Display Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Latest Gold Spot Price", f"${latest_price:,.2f}", f"{change:+.2f} USD")
    col2.metric("24h High", f"${df['High'].max():,.2f}")
    col3.metric("24h Low", f"${df['Low'].min():,.2f}")

    st.subheader("Gold Price Movement")
    st.line_chart(df['Close'])

    # Basic Analysis Engine
    st.subheader("📊 Market Structure Summary")
    high_max = df['High'].tail(10).max()
    low_min = df['Low'].tail(10).min()

    st.write(f"- **Recent High (Resistance):** ${high_max:,.2f}")
    st.write(f"- **Recent Low (Support):** ${low_min:,.2f}")
    
    if latest_price > high_max * 0.998:
        st.success("🔥 Price is approaching recent resistance levels (Bullish Momentum).")
    elif latest_price < low_min * 1.002:
        st.warning("⚠️ Price is testing recent support levels (Bearish Pressure).")
    else:
        st.info("⚖️ Price is currently consolidating inside the range.")
else:
    st.error("Failed to load Gold market data. Please try changing the period or interval.")
