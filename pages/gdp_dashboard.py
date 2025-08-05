import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

st.set_page_config(page_title="World GDP", page_icon="🌍", layout="wide")
st.title("🌍 GDP & FX Explorer")

@st.cache_data
def load_gdp():
    df = pd.read_csv("data/gdp_data.csv")
    years = [str(y) for y in range(1960, 2023)]
    df_long = df.melt(id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
                      value_vars=years,
                      var_name="Year",
                      value_name="GDP")
    df_long["Year"] = pd.to_numeric(df_long["Year"])
    df_long["GDP"] = pd.to_numeric(df_long["GDP"], errors="coerce")
    df_long = df_long.dropna(subset=["GDP"])
    return df_long

gdp_df = load_gdp()

countries = sorted(gdp_df["Country Name"].unique())
selected_country = st.selectbox("Select a country", countries)
country_data = gdp_df[gdp_df["Country Name"] == selected_country]

fig = px.line(country_data, x="Year", y="GDP", title=f"GDP Over Time: {selected_country}", labels={"GDP": "GDP (current US$)"})
st.plotly_chart(fig, use_container_width=True)

st.dataframe(country_data[["Year", "GDP"]].reset_index(drop=True))

st.header("💱 Currency Valuation")

currencies = [
    "USD", "EUR", "JPY", "GBP", "AUD",
    "CAD", "CHF", "CNY"
]
base_currency = st.selectbox("Base Currency", currencies)
quote_currency = st.selectbox("Quote Currency", currencies, index=currencies.index("USD"))

if base_currency == quote_currency:
    st.warning("Select two different currencies for comparison.")
else:
    pair_symbol = f"{base_currency}{quote_currency}=X"
    fx_data = yf.download(pair_symbol, period="5y")
    if fx_data.empty:
        st.error("No data available for the selected currency pair.")
    else:
        fig_fx = px.line(
            fx_data,
            x=fx_data.index,
            y="Close",
            title=f"{base_currency}/{quote_currency} Exchange Rate",
            labels={"Close": "Exchange Rate"}
        )
        st.plotly_chart(fig_fx, use_container_width=True)
        st.dataframe(
            fx_data[["Close"]]
            .rename(columns={"Close": f"{base_currency}/{quote_currency}"})
            .reset_index()
        )
