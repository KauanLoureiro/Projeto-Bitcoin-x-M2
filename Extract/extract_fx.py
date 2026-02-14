# %%
import pandas as pd
import yfinance as yf 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

tickers = ["EURUSD=X", "JPYUSD=X", "CNYUSD=X"]
data = yf.download(tickers=tickers, start="2017-01-01")
BRONZE_PATH = BASE_DIR / "Data" / "Bronze" / "fx.csv"
data.to_csv(BRONZE_PATH)

# # %%
# data_close = data["Close"]
# data_close.reset_index(inplace=True)
# data_close.columns = ["Date", "CNYUSD", "EURUSD", "JPYUSD"]
# # data_close.sort_values("Date", ascending=False, inplace=True)

# # %%

# data_close.to_csv(BRONZE_PATH, index=False)
# # %%
# data_close