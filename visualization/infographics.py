import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from data.scrape import *
import plotly.graph_objects as go
import numpy as np

def mcap_ig(df):
    top_df = df.head(5)
    # Log transform market caps and normalize
    top_df['log_cap'] = np.log10(top_df['market_cap'])-10
    max_log_cap = top_df['log_cap'].max()



    top_df['size'] = top_df['log_cap'] / max_log_cap  # scaled to 0–1

    top_df.loc[:, 'x'] = range(len(top_df))  # Even spacing
    top_df.loc[:, 'y'] = [1] * len(top_df)

    # print(top_df)

    # Create Plotly figure
    fig = go.Figure()

    # Add logos as images
    for _, row in top_df.iterrows():
        fig.add_layout_image(
            dict(
                source=row['image'],
                xref="x", yref="y",
                x=row['x'], y=row['y'],
                sizex=row['size'], sizey=row['size'],
                xanchor="center", yanchor="middle",
                layer="above"
            )
        )

    # Dummy trace for layout
    fig.add_trace(go.Scatter(
        x=top_df['x'],
        y=top_df['y'],
        mode='markers+text',
        text=top_df['name'],
        textposition="bottom center",
        marker=dict(size=1, opacity=0)
    ))

    fig.update_xaxes(visible=False, range=[-1, len(top_df)])
    fig.update_yaxes(visible=False, range=[0, 2])

    fig.update_layout(
        title="Top 5 Cryptos by Market Cap (Logo Size = log₁₀(Market Cap))",
        width=800,
        height=400,
        margin=dict(l=0, r=0, t=40, b=0)
    )

    # Display in Streamlit
    return fig



def upvote_ratio(df):
    df_top10 = df.head(10).copy()
    df_top10["mention_upvote_ratio"] = df_top10["mentions"] / df_top10["upvotes"]
    df_sorted = df_top10.sort_values(by="mention_upvote_ratio", ascending=False)
    # Plot with custom color gradient (green = good, red = bad)
    # st.subheader("Mention-to-Upvote Ratio (Top 10 Tickers)")
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

    return fig