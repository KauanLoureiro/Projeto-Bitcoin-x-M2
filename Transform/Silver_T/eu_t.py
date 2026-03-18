#%%
from conn import con, bronze
import pandas as pd
from io import StringIO
import json

conection = con()
bronze_path = bronze()

eu_path = bronze_path / "M2_eu.json"

with open(eu_path, "r") as f:
    eu = json.load(f)

# Formatação para entrar no SQL
dates_list = eu['structure']["dimensions"]["observation"][0]["values"]
date = []
for j in dates_list:
    date.append(j[list(j.keys())[0]])

obs = eu['dataSets'][0]['series']['0:0:0:0:0:0:0:0:0:0:0']['observations']
value = []
for i in list(obs.keys()):
    value.append(obs[i][0])

df_eu = pd.DataFrame({
    "Date":date,
    "M2_eu":value
})
df_eu["M2_eu"] = (10**6)*(df_eu["M2_eu"])

df_eu["Date"] = pd.to_datetime(df_eu["Date"])

df_eu["YearMonth"] = df_eu["Date"].dt.to_period("M").astype(str)

df_eu = df_eu.groupby("YearMonth", as_index=False).agg({
    "M2_eu": "mean"
})
df_eu.sort_values("YearMonth", ascending=False, inplace=True)

#Jogando para a memoria para fzr o copy
buffer = StringIO()
df_eu.to_csv(buffer, index=False, header=True)
buffer.seek(0)

#Mexendo no DB
cur = conection.cursor()

cur.execute(""" 
             CREATE TABLE IF NOT EXISTS silver.m2_eu_eur(
             yearmonth TEXT,
             M2_eu FLOAT
            ); 
            """)

cur.execute("TRUNCATE TABLE silver.m2_eu_eur;")

cur.copy_expert(
    sql="COPY silver.m2_eu_eur FROM STDIN WITH CSV HEADER",
    file=buffer
)

conection.commit()
cur.close()
conection.close()