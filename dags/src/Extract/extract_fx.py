# %%
import pandas as pd
import yfinance as yf 

def extract_fx():
    tickers = ["EURUSD=X", "JPYUSD=X", "CNYUSD=X"]
    data = yf.download(tickers=tickers, start="2017-01-01")
    return data

