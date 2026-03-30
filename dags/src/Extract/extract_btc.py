# %%
import ccxt
import pandas as pd

def extract_btc():

    exchange = ccxt.kraken()
    exchange.load_markets()
    since = exchange.parse8601(pd.to_datetime("2017/01/01"))

    data = exchange.fetch_ohlcv("BTC/USD", timeframe="1w", since=since)

    df = pd.DataFrame(data, columns=['timestamp','open','high','low','close','volume'])

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df
