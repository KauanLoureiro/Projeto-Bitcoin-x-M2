# %%

import pandas as pd
import sqlite3
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parents[2]

DB_path = BASE_DIR / "Data" / "Silver" / "Silver_raw.db"
bronze_path = BASE_DIR / "Data" / "Bronze"

con = sqlite3.connect(DB_path)

def sort(x):
    x.sort_values("Date", ascending=False, inplace=True)
    return

# %%
# Bitcoin ✓

btc_path = bronze_path / "Bitcoin_raw.csv"

btc = pd.read_csv(btc_path)

btc = btc[["timestamp", "close"]]

btc = btc.rename(columns={
    "timestamp":"Date",
    "close" : "BTC_price"
})
btc["Date"] = pd.to_datetime(btc["Date"])
sort(btc)
# btc.sort_values("Date", ascending=False, inplace=True)

btc.to_sql("BTC", con=con, if_exists="replace", index=False)
# %%
# Europa

eu_path = bronze_path / "M2_eu.json"

with open(eu_path, "r") as f:
    eu = json.load(f)

# Formatação para entrar no SQL
dates_list = eu['structure']["dimensions"]["observation"][0]["values"]
date = []
for j in dates_list:
    date.append(j[list(j.keys())[0]])

obs = eu['dataSets'][0]['series']['0:0:0:0:0:0:0:0:0:0:0']['observations']
value = []
for i in list(obs.keys()):
    value.append(obs[i][0])

df_eu = pd.DataFrame({
    "Date":date,
    "M2_eu":value
})
df_eu["M2_eu"] = (10**6)*(df_eu["M2_eu"])

df_eu["Date"] = pd.to_datetime(df_eu["Date"])

sort(df_eu)

#falta converter de euro para dolar
df_eu.to_sql("M2_eu", con=con, if_exists="replace", index=False)
# %%
# US ✓

us_path = bronze_path / "M2_us.json"

with open(us_path, "r") as f:
    us = json.load(f)

j = []

for i in us['observations']:
    j.append({
        "date": i["date"],
        "value": i["value"]
    })
 
df_us = pd.DataFrame(j)

df_us["date"] = pd.to_datetime(df_us["date"])
df_us["value"] = (10**9)*(pd.to_numeric(df_us["value"]))
df_us = df_us.rename(columns={"date":"Date",
                              "value":"M2_us"})

sort(df_us)

df_us.to_sql("M2_us",con=con,if_exists="replace", index=False)
# %%
# JAPAN
JP_PATH = bronze_path / "M2_jp.csv"

jp = pd.read_csv(JP_PATH)

jp = jp[["0", "9"]].drop(jp.index[0:7]).rename(columns={
    "0":"Date",
    "9":"M2_jp"
})

jp["Date"] = pd.to_datetime(jp["Date"])
jp.dropna(how="any")

jp = jp.query("M2_jp != 'ND'")
jp["M2_jp"] = pd.to_numeric(jp["M2_jp"])*10**8
sort(jp)

jp.to_sql("M2_jp", con=con, if_exists="replace", index=False)
#falta converter de iene para dolar

# %%

cn_path = bronze_path / "M2_cn.json"

with open(cn_path, "r", encoding="utf-8") as f:
    cn = json.load(f)


def format(df):
    df = pd.DataFrame(df)
    df = df.T
    df = df[[4,6]]
    df.index = range(0 , len(df))
    df = df.drop([0,1,2])
    df = df.rename(columns={
        4:"Date",
        6:"M2_cn"
    })
    df["Date"] = pd.to_datetime(df["Date"].astype(str))
    df.loc[12,"Date"] = df.loc[12,"Date"].replace(month=10)
    df = df.sort_values(by="Date", ascending=False)
    return df

cn_format = []

for i in cn:
    cn_format.append(format(i))

M2_cn = pd.concat(cn_format, axis=0, ignore_index=True)
M2_cn.dropna(inplace=True)
sort(M2_cn)

M2_cn.to_sql("M2_cn", con=con, if_exists="replace", index=False)
#falta converter de yuan para dolar

# %%

fx_path = bronze_path / "fx.csv"

fx = pd.read_csv(fx_path)

fx_close = fx[list(fx.columns)[0:4]]
fx_close.columns = ["Date", "CNYUSD", "EURUSD", "JPYUSD"]
fx_close = fx_close.drop([0,1])
fx_close.sort_values("Date", ascending=False, inplace=True)
fx_close["Date"] = pd.to_datetime(fx_close["Date"])

fx_close.to_sql("fx", con=con, if_exists="replace", index=False)


# %%
