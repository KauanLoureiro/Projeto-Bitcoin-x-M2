import pandas as pd

def load_m2_jp_bronze(df:pd.DataFrame):
    df.to_csv("/opt/airflow/data/Bronze/M2_jp.csv", index=False)