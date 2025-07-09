import requests
import pandas as pd

def fetch_apewisdom_data():
    url = "https://apewisdom.io/api/v1.0/filter/all"
    response = requests.get(url)
    data = response.json()

    tickers = data.get("results", [])
    df = pd.DataFrame(tickers)
    return df

def fetch_coingecko_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": "false"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Failed to fetch Coingecko data:", response.status_code)
        return pd.DataFrame()

    data = response.json()
    df = pd.DataFrame(data)
    return df