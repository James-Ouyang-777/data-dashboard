# pages/fdgfdgfdg.py
import streamlit as st
from visualization.helpers import render_live_price_chart
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Live Crypto Dashboard",
    page_icon="📈",
    layout="wide"
)
st.title("📡 Live Crypto Chart")
st_autorefresh(interval=3000, limit=None, key="autorefresh")

render_live_price_chart(symbol="PERP_BTC_USDC")


# import streamlit as st
# import pandas as pd
# import plotly.graph_objs as go
# import time
# import requests
# from streamlit_autorefresh import st_autorefresh

# # --- CONFIG ---
# st.set_page_config(page_title="Live Crypto Dashboard", page_icon="📈", layout="wide")
# st.title("📡 Live Crypto Chart")
# symbol = "PERP_BTC_USDC"

# # --- STATE INIT ---
# if "live_data" not in st.session_state:
#     st.session_state.live_data = []
#     st.session_state.start_time = time.time()
# if "streaming" not in st.session_state:
#     st.session_state.streaming = False

# # --- GET PRICE ---
# def get_orderly_price(symbol):
#     try:
#         url = f"https://api-evm.orderly.org/v1/public/futures/{symbol}"
#         response = requests.get(url)
#         data = response.json()["data"]
#         return data["mark_price"], data["index_price"]
#     except:
#         return None, None

# # --- STREAM CONTROLS ---
# col1, col2 = st.columns([1, 5])
# with col1:
#     if st.button("▶️ Start") and not st.session_state.streaming:
#         st.session_state.streaming = True
#     if st.button("⏹️ Stop") and st.session_state.streaming:
#         st.session_state.streaming = False

# # --- AUTOREFRESH ONLY WHEN STREAMING ---
# if st.session_state.streaming:
#     st_autorefresh(interval=1000, limit=None, key="stream-autorefresh")

# # --- DATA UPDATE ---
# if st.session_state.streaming:
#     mark, index = get_orderly_price(symbol)
#     if mark is not None and index is not None:
#         elapsed = round(time.time() - st.session_state.start_time, 2)
#         st.session_state.live_data.append({
#             "Time": elapsed,
#             "Mark Price": mark,
#             "Index Price": index
#         })
#         st.session_state.live_data = st.session_state.live_data[-200:]

# # --- PLOT ---
# df = pd.DataFrame(st.session_state.live_data)
# if not df.empty:
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=df["Time"], y=df["Mark Price"], mode="lines", name="Mark Price"))
#     fig.add_trace(go.Scatter(x=df["Time"], y=df["Index Price"], mode="lines", name="Index Price"))
#     fig.update_layout(height=400, xaxis_title="Time (s)", yaxis_title="Price")
#     st.plotly_chart(fig, use_container_width=True)
# else:
#     st.info("Click ▶️ Start to begin live streaming.")
