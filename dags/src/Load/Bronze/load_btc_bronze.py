import pandas as pd

def load_btc_bronze(df:pd.DataFrame):
    df.to_csv("/opt/airflow/data/Bronze/Bitcoin_raw.csv", index=False)