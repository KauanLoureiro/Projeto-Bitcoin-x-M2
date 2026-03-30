#%%
import pandas as pd
from io import StringIO
from pathlib import Path
from airflow.providers.postgres.hooks.postgres import PostgresHook

def extract_jp_silver():
    bronze_path = Path("/opt/airflow/data/Bronze")

    JP_PATH = bronze_path / "M2_jp.csv"

    return pd.read_csv(JP_PATH)

def transform_jp_silver(jp):
    jp = jp[["0", "9"]].drop(jp.index[0:7]).rename(columns={
        "0":"Date",
        "9":"M2_jp"
    })

    jp["Date"] = pd.to_datetime(jp["Date"])
    jp.dropna(how="any")

    jp = jp.query("M2_jp != 'ND'")
    jp["M2_jp"] = pd.to_numeric(jp["M2_jp"])*10**8

    jp["YearMonth"] = jp["Date"].dt.to_period("M").astype(str)

    jp = jp.groupby("YearMonth", as_index=False).agg({
        "M2_jp": "mean"
    })
    jp = jp.sort_values("YearMonth", ascending=False)
    return jp

def load_jp_silver(jp):
#Jogando para a memoria para fzr o copy
    buffer = StringIO()
    jp.to_csv(buffer, index=False, header=True)
    buffer.seek(0)

    #Mexendo no DB
    hook = PostgresHook(postgres_conn_id="postgres_dw")
    conn = hook.get_conn()
    cur = conn.cursor()

    cur.execute("CREATE SCHEMA IF NOT EXISTS silver;")

    cur.execute(""" 
                CREATE TABLE IF NOT EXISTS silver.m2_jp_jpy(
                yearmonth TEXT,
                M2_jp FLOAT
                ); 
                """)

    cur.execute("TRUNCATE TABLE silver.m2_jp_jpy;")

    cur.copy_expert(
        sql="COPY silver.m2_jp_jpy FROM STDIN WITH CSV HEADER",
        file=buffer
    )

    conn.commit()
    cur.close()
    conn.close()