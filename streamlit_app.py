import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from data.scrape import *

st.title("Reddit: Top 10 Trending Tickers")
df = fetch_apewisdom_data()
df.set_index('rank', inplace=True)
df = df.head(10).copy()
df_top10 = df.head(10).copy()
df_top10["mention_upvote_ratio"] = df_top10["mentions"] / df_top10["upvotes"]
df_sorted = df_top10.sort_values(by="mention_upvote_ratio", ascending=False)

# Display table
st.dataframe(df)

# Plot with custom color gradient (green = good, red = bad)
st.subheader("Mention-to-Upvote Ratio (Top 10 Tickers)")
fig = px.bar(
    df_sorted,
    x="ticker",
    y="mention_upvote_ratio",
    color="mention_upvote_ratio",
    color_continuous_scale="RdYlGn",  # Red -> Yellow -> Green
    labels={"mention_upvote_ratio": "Mentions / Upvotes"},
    title="Mention-to-Upvote Ratio by Ticker",
    text="mention_upvote_ratio"
)

fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
fig.update_layout(
    yaxis=dict(title="Ratio"),
    xaxis=dict(title="Ticker"),
    coloraxis_colorbar=dict(title="Ratio"),
    uniformtext_minsize=8
)

st.plotly_chart(fig, use_container_width=True)



# st.dataframe(df)


# ticker = st.text_input("Enter a stock ticker (e.g., AAPL)")

# if ticker:
    # st.write(f"Showing data for {ticker}")
    
    # Placeholder: Load from local CSV or scrape data

    
    # # Example: Top holders
    # top_holders = df.sort_values("Market Value", ascending=False).head(10)
    # fig, ax = plt.subplots()
    # ax.barh(top_holders["Fund"], top_holders["Market Value"])
    # st.pyplot(fig)

