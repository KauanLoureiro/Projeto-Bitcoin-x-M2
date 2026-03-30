import pandas as pd
from io import StringIO
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pathlib import Path


def extract_btc_silver():
    bronze_path = Path("/opt/airflow/data/Bronze")

    btc_path = bronze_path / "Bitcoin_raw.csv"

    return pd.read_csv(btc_path)

def transform_btc_silver(btc):
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

    btc = btc.sort_values("YearMonth", ascending=False)
    return btc

def load_btc_silver(btc):
    #Jogando para a memoria para fzr o copy
    buffer = StringIO()
    btc.to_csv(buffer, index=False, header=True)
    buffer.seek(0)

    hook = PostgresHook(postgres_conn_id="postgres_dw")
    conn = hook.get_conn()
    cur = conn.cursor()

    cur.execute("CREATE SCHEMA IF NOT EXISTS silver;")

    cur.execute(""" 
             CREATE TABLE IF NOT EXISTS silver.btc_dol(
             yearmonth TEXT,
             BTC_price FLOAT
            ); 
            """)

    cur.execute("TRUNCATE TABLE silver.btc_dol;")

    # COPY via hook
    cur.copy_expert(
        sql="COPY silver.btc_dol FROM STDIN WITH CSV HEADER",
        file=buffer
    )

    conn.commit()
    cur.close()
    conn.close()