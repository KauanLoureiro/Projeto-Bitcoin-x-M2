import pandas as pd

def load_fx_bronze(df:pd.DataFrame):
    df.to_csv("/opt/airflow/data/Bronze/fx.csv")