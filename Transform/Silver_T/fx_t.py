#%%
from conn import con, bronze
import pandas as pd
from io import StringIO

conection = con()
bronze_path = bronze()

fx_path = bronze_path / "fx.csv"

fx = pd.read_csv(fx_path)

fx = fx[list(fx.columns)[0:4]]
fx.columns = ["Date", "CNYUSD", "EURUSD", "JPYUSD"]
fx = fx.drop([0,1])
fx.sort_values("Date", ascending=False, inplace=True)
fx["Date"] = pd.to_datetime(fx["Date"])
fx.dropna(how="any", inplace=True)

fx["YearMonth"] = fx["Date"].dt.to_period("M").astype(str)

fx["CNYUSD"] = pd.to_numeric(fx["CNYUSD"])
fx["EURUSD"] = pd.to_numeric(fx["EURUSD"])
fx["JPYUSD"] = pd.to_numeric(fx["JPYUSD"])

fx = fx.groupby("YearMonth", as_index=False).agg({
    "CNYUSD": "mean",
    "EURUSD": "mean",
    "JPYUSD": "mean"

})
fx.sort_values("YearMonth", ascending=False, inplace=True)

#Jogando para a memoria para fzr o copy
buffer = StringIO()
fx.to_csv(buffer, index=False, header=True)
buffer.seek(0)

#Mexendo no DB
cur = conection.cursor()

cur.execute(""" 
             CREATE TABLE IF NOT EXISTS silver.fx(
             yearmonth TEXT,
             cnyusd FLOAT,
             eurusd FLOAT,
             jpyusd FLOAT
            ); 
            """)

cur.execute("TRUNCATE TABLE silver.fx;")

cur.copy_expert(
    sql="COPY silver.fx FROM STDIN WITH CSV HEADER",
    file=buffer
)

conection.commit()
cur.close()
conection.close()