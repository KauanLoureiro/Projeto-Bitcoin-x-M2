import requests
import pandas as pd
import sqlite3
import os
import json
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = BASE_DIR / "Environment" / "API_key.env"

print(os.getcwd())

# Testar "..\environment\API_key.env"
load_dotenv(dotenv_path=ENV_PATH)

FRED_API_KEY = os.getenv("FRED_KEY")

def get_M2(id_serie):
    url_base_EUA = "https://api.stlouisfed.org/fred/series/observations"

    con = requests.get(
        url=url_base_EUA, 
        params={
            "series_id": id_serie,
            "api_key": FRED_API_KEY,
            "file_type": "json"
            }
        )
    
    if con.status_code == 200:
        print("Success")
    else:
        print(f"status error: {con.status_code}")

    return con.json()

Id = {"EUA": "M2SL"}

data_EUA = get_M2(Id["EUA"])

BRONZE_PATH = BASE_DIR / "Data" / "Bronze" / "M2_us.json"

with open(BRONZE_PATH, "w", encoding="utf-8") as f:
    json.dump(
        data_EUA,
        f
    )

# df = pd.DataFrame(data_EUA)
# df.to_csv(BRONZE_PATH)