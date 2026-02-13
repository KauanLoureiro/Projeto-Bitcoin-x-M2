# %%
import ccxt
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

exchange = ccxt.kraken()
exchange.load_markets()

# %%
since = exchange.parse8601(pd.to_datetime("2017/01/01"))

data = exchange.fetch_ohlcv("BTC/USD", timeframe="1w", since=since)

data

df = pd.DataFrame(data, columns=['timestamp','open','high','low','close','volume'])

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

BRONZE_PATH = BASE_DIR / "Data" / "Bronze" / "Bitcoin_raw.csv"

df.to_csv(BRONZE_PATH, index=False)
# %%
