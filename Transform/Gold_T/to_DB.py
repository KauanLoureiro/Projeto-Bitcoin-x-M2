# %%
import sqlite3
import pandas as pd
from pathlib import Path 

BASE_DIR = Path(__file__).resolve().parents[2]
GOLD_PATH = BASE_DIR / "Data" / "Gold" / "Gold.db"
SILVER_PATH = BASE_DIR / "Data" / "sILVER" / "Silver.db"

con_silver = sqlite3.connect(SILVER_PATH)
con_gold = sqlite3.connect(GOLD_PATH)

with open("M2_global.sql", "r") as f:
    M2_global_query = f.read()

with open("BTC_m.sql", "r") as f:
    BTC_m_query = f.read()

M2_global = pd.read_sql_query(M2_global_query, con=con_silver)
BTC_m = pd.read_sql_query(BTC_m_query, con=con_silver)

M2_global.to_sql("M2_global", con=con_gold, if_exists="replace", index=False)
BTC_m.to_sql("BTC_DOL", con=con_gold, if_exists="replace", index=False)

# %%
