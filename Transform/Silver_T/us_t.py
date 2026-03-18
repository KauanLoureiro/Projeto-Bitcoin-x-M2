#%%
from conn import con, bronze
import pandas as pd
from io import StringIO
import json

conection = con()
bronze_path = bronze()

us_path = bronze_path / "M2_us.json"

with open(us_path, "r") as f:
    us = json.load(f)

j = []

for i in us['observations']:
    j.append({
        "date": i["date"],
        "value": i["value"]
    })
 
df_us = pd.DataFrame(j)

df_us["date"] = pd.to_datetime(df_us["date"])
df_us["value"] = (10**9)*(pd.to_numeric(df_us["value"]))
df_us = df_us.rename(columns={"date":"Date",
                              "value":"M2_us"})

df_us["YearMonth"] = df_us["Date"].dt.to_period("M").astype(str)

df_us = df_us.groupby("YearMonth", as_index=False).agg({
    "M2_us": "mean"
})
df_us.sort_values("YearMonth", ascending=False, inplace=True)

#Jogando para a memoria para fzr o copy
buffer = StringIO()
df_us.to_csv(buffer, index=False, header=True)
buffer.seek(0)

#Mexendo no DB
cur = conection.cursor()

cur.execute(""" 
             CREATE TABLE IF NOT EXISTS silver.m2_us_dol(
             YearMonth TEXT,
             M2_us FLOAT
            ); 
            """)

cur.execute("TRUNCATE TABLE silver.m2_us_dol;")

cur.copy_expert(
    sql="COPY silver.m2_us_dol FROM STDIN WITH CSV HEADER",
    file=buffer
)

conection.commit()
cur.close()
conection.close()