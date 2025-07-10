# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from data.scrape import *
import plotly.graph_objects as go
from visualization.helpers import *
from visualization.infographics import *



st.set_page_config(page_title="Home", page_icon="🏠", layout='wide')
# st.title("🏠 Home Dashboard")

# Fetch data
df = fetch_apewisdom_data()
df2 = fetch_coingecko_data()

# Prepare DataFrame 1 (Ape Wisdom)
df.set_index('rank', inplace=True)
df = df.head(10).copy()

# Prepare DataFrame 2 (Coingecko)
raw_crypto_data = df2.copy()
raw_crypto_data = raw_crypto_data.drop(columns=["image"])


# --- Row 1: Graphs side by side ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Reddit: Top 10 Trending Tickers")
    st.plotly_chart(upvote_ratio(df), use_container_width=True, key=f"chart_{int(time.time())}")

with col2:
    st.subheader("Top Cryptos by Market Cap")
    st.plotly_chart(mcap_ig(df2), use_container_width=True, key="market_cap_infographic")

# --- Row 2: DataFrames side by side ---
col4, col5 = st.columns(2)

with col4:
    st.dataframe(df)

with col5:
    st.dataframe(raw_crypto_data)
