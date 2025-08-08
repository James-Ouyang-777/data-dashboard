import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

st.set_page_config(
    page_title="Options Volatility Surface",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Options Volatility Surface")

@st.cache_data
def load_option_data(symbol: str, max_expirations: int = 4) -> pd.DataFrame:
    ticker = yf.Ticker(symbol)
    try:
        expirations = ticker.options[:max_expirations]
    except Exception:
        return pd.DataFrame(columns=["strike", "impliedVolatility", "expiration"])
    frames = []
    for exp in expirations:
        try:
            chain = ticker.option_chain(exp)
            calls = chain.calls[["strike", "impliedVolatility"]].copy()
            calls["expiration"] = exp
            frames.append(calls)
        except Exception:
            continue
    if frames:
        return pd.concat(frames, ignore_index=True)
    return pd.DataFrame(columns=["strike", "impliedVolatility", "expiration"])

symbol = st.text_input("Ticker", "AAPL").upper().strip()
max_exp = st.slider("Number of Expirations", 1, 10, 4)

if symbol:
    data = load_option_data(symbol, max_exp)
    if data.empty:
        st.error("No options data available.")
    else:
        pivot = data.pivot_table(index="strike", columns="expiration", values="impliedVolatility")
        pivot.sort_index(inplace=True)
        x = [str(c) for c in pivot.columns]
        y = pivot.index.values
        z = pivot.values
        fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale="Viridis")])
        fig.update_layout(
            height=700,
            scene=dict(
                xaxis_title="Expiration",
                yaxis_title="Strike",
                zaxis_title="Implied Volatility"
            ),
            title=f"{symbol} Implied Volatility Surface"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(data)
