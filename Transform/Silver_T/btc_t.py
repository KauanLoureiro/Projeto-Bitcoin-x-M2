#%%
from conn import con, bronze
import pandas as pd
from io import StringIO

conection = con()
bronze_path = bronze()

btc_path = bronze_path / "Bitcoin_raw.csv"

btc = pd.read_csv(btc_path)

btc = btc[["timestamp", "close"]]

btc = btc.rename(columns={
    "timestamp":"Date",
    "close" : "BTC_price"
})
btc["Date"] = pd.to_datetime(btc["Date"])

btc["YearMonth"] = btc["Date"].dt.to_period("M").astype(str)

btc = btc.groupby("YearMonth", as_index=False).agg({
    "BTC_price": "mean"
})
btc.sort_values("YearMonth", ascending=False, inplace=True)

#Jogando para a memoria para fzr o copy
buffer = StringIO()
btc.to_csv(buffer, index=False, header=True)
buffer.seek(0)

#Mexendo no DB
cur = conection.cursor()

cur.execute(""" 
             CREATE TABLE IF NOT EXISTS silver.btc_dol(
             yearmonth TEXT,
             BTC_price FLOAT
            ); 
            """)

cur.execute("TRUNCATE TABLE silver.btc_dol;")

cur.copy_expert(
    sql="COPY silver.btc_dol FROM STDIN WITH CSV HEADER",
    file=buffer
)

conection.commit()
cur.close()
conection.close()
# %%
