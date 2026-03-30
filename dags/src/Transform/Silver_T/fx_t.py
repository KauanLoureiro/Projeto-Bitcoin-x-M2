#%%
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
from io import StringIO
from pathlib import Path

def extract_fx_silver():
    bronze_path = Path("/opt/airflow/data/Bronze")
    fx_path = bronze_path / "fx.csv"
    return pd.read_csv(fx_path)

def transform_fx_silver(fx):
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
    fx = fx.sort_values("YearMonth", ascending=False)
    return fx

def load_fx_silver(fx):
    #Jogando para a memoria para fzr o copy
    buffer = StringIO()
    fx.to_csv(buffer, index=False, header=True)
    buffer.seek(0)

    #Mexendo no DB
    hook = PostgresHook(postgres_conn_id="postgres_dw")
    conn = hook.get_conn()
    cur = conn.cursor()

    cur.execute("CREATE SCHEMA IF NOT EXISTS silver;")

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

    conn.commit()
    cur.close()
    conn.close()