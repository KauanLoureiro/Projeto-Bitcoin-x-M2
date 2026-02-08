import pandas as pd
import requests
import os
from dotenv import load_dotenv
from io import StringIO, BytesIO

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