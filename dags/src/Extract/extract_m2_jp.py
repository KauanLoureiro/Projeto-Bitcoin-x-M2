import pandas as pd
import requests
from io import StringIO

def extract_m2_jp():
    url_base_JAP = "https://www.stat-search.boj.or.jp/ssi/mtshtml/md02_m_1_en.html"

    con = requests.get(url_base_JAP)

    if con.status_code == 200:
        print("Success")
    else:
        print(f"status error: {con.status_code}")

    data_japan = pd.read_html(StringIO(con.text))

    df = data_japan[0]

    return df

# BASE_DIR = Path(__file__).resolve().parents[1]
# BRONZE_PATH = BASE_DIR / "Data" / "Bronze" / "M2_jp.csv"

# df.to_csv(BRONZE_PATH)