import requests
import pandas as pd

def fetch_apewisdom_data():
    url = "https://apewisdom.io/api/v1.0/filter/all"
    response = requests.get(url)
    data = response.json()

    tickers = data.get("results", [])
    df = pd.DataFrame(tickers)
    return df