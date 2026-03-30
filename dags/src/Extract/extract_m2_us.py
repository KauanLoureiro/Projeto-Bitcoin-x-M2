import requests
import os
import json
from dotenv import load_dotenv

# load_dotenv(dotenv_path="/opt/airflow/.env")

FRED_API_KEY = os.getenv("FRED_KEY")

def get_M2(id_serie):
    url_base_EUA = "https://api.stlouisfed.org/fred/series/observations"

    con = requests.get(
        url=url_base_EUA, 
        params={
            "series_id": id_serie,
            "api_key": FRED_API_KEY,
            "file_type": "json"
            },
        timeout=10
        )
    
    if con.status_code == 200:
        print("Success")
    else:
        print(f"status error: {con.status_code}")

    return con.json()

def extract_m2_us():
    Id = {"EUA": "M2SL"}
    return get_M2(Id["EUA"])