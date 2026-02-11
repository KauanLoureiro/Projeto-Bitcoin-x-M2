import requests
import pandas as pd
import sqlite3
import json
from pathlib import Path

url_base_EUR = "https://data-api.ecb.europa.eu/service/data/BSI/M.U2.Y.V.M20.X.1.U2.2300.Z01.E"

headers = {
    "Accept": "application/json"
}

response = requests.get(url_base_EUR, headers=headers)

if response.status_code == 200:
    print("Success")
else:
    print(f"status error: {response.status_code}")

data_EURO = response.json()

BASE_DIR = Path(__file__).resolve().parents[1]
BRONZE_PATH = BASE_DIR / "Data" / "Bronze" / "M2_eu.json"

with open(BRONZE_PATH, "w", encoding="utf-8") as f:
    json.dump(
        data_EURO,
        f,
        ensure_ascii=False,
        indent=2
    )

# # Formatação para entrar no SQL
# dates_list = data_EURO['structure']["dimensions"]["observation"][0]["values"]
# date = []
# for j in dates_list:
#     date.append(j[list(j.keys())[0]])

# obs = data_EURO['dataSets'][0]['series']['0:0:0:0:0:0:0:0:0:0:0']['observations']
# value = []
# for i in list(obs.keys()):
#     value.append(obs[i][0])

# df = pd.DataFrame({
#     "Dates":date,
#     "M2_eu_value":value
# })

