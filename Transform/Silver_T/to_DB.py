# %%

import pandas as pd
import sqlite3
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parents[2]

DB_path = BASE_DIR / "Data" / "Silver" / "Silver_raw.db"
bronze_path = BASE_DIR / "Data" / "Bronze"

con = sqlite3.connect(DB_path)

# %%
# Bitcoin

btc_path = bronze_path / "Bitcoin_raw.csv"

btc = pd.read_csv(btc_path)

btc.to_sql("BTC", con=con, if_exists="replace")
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
    "Dates":date,
    "M2_eu_value":value
})

df_eu.to_sql("M2_eu", con=con, if_exists="replace")
# %%
# US

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
df_us = df_us.rename(columns={"value":"M2_us"})

df_us.to_sql("M2_us",con=con,if_exists="replace")
# %%
