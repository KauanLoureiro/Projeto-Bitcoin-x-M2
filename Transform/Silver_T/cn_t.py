#%%
from conn import con, bronze
import pandas as pd
from io import StringIO
import json

conection = con()
bronze_path = bronze()

def get_date(x):
    if type(x) == str:
        return x[:-1]
    else:
        return x
    
def get_m2(x):
    if type(x) == str:
        return x[:-1]
    else:
        return x

cn_path = bronze_path / "M2_cn.json"

with open(cn_path, "r", encoding="utf-8") as f:
    cn = json.load(f)

def format(df):
    df = pd.DataFrame(df)
    df = df.T
    df = df[[4,6]]
    df.index = range(0 , len(df))
    df = df.drop([0,1,2])
    df = df.rename(columns={
        4:"Date",
        6:"M2_cn"
    })
    df["Date"] = df["Date"].apply(get_date)
    df["M2_cn"] = df["M2_cn"].apply(get_m2)
    df["Date"] = pd.to_datetime(df["Date"].astype(str))
    df.loc[12,"Date"] = df.loc[12,"Date"].replace(month=10)
    df = df.sort_values(by="Date", ascending=False)
    return df

cn_format = []

for i in cn:
    cn_format.append(format(i))

M2_cn = pd.concat(cn_format, axis=0, ignore_index=True)
M2_cn.dropna(inplace=True)
M2_cn["M2_cn"] = pd.to_numeric(M2_cn["M2_cn"])*10**9

M2_cn["YearMonth"] = M2_cn["Date"].dt.to_period("M").astype(str)

M2_cn = M2_cn.groupby("YearMonth", as_index=False).agg({
    "M2_cn": "mean"
})
M2_cn.sort_values("YearMonth", ascending=False, inplace=True)

#Jogando para a memoria para fzr o copy
buffer = StringIO()
M2_cn.to_csv(buffer, index=False, header=True)
buffer.seek(0)

#Mexendo no DB
cur = conection.cursor()

cur.execute(""" 
             CREATE TABLE IF NOT EXISTS silver.m2_cn_cny(
             yearmonth TEXT,
             M2_cn FLOAT
            ); 
            """)

cur.execute("TRUNCATE TABLE silver.m2_cn_cny;")

cur.copy_expert(
    sql="COPY silver.m2_cn_cny FROM STDIN WITH CSV HEADER",
    file=buffer
)

conection.commit()
cur.close()
conection.close()
# %%
