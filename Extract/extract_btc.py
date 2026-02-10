import requests
import pandas as pd

url_base_BTC = "https://api.coinpaprika.com/v1/tickers"

response = requests.get(url=url_base_BTC)

if response.status_code == 200:
    print("Success")
else:
    print(f"status error: {response.status_code}")

db = response.json()


for i in db:
    if i["symbol"].lower() == "btc":
        data_BTC = i
        break
