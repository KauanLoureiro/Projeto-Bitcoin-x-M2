import pandas as pd
import requests
from io import StringIO

url_base_JAP = "https://www.stat-search.boj.or.jp/ssi/mtshtml/md02_m_1_en.html"

con = requests.get(url_base_JAP)

if con.status_code == 200:
    print("Success")
else:
    print(f"status error: {con.status_code}")

data_japan = pd.read_html(StringIO(con.text))
