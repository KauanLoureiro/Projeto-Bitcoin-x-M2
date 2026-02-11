import pandas as pd
import requests
import sqlite3
import json
from pathlib import Path
from io import BytesIO

file = {
    2025:"https://www.pbc.gov.cn/diaochatongjisi/attachDir/2025/11/2025111913535649624.xlsx",
    2024:"https://www.pbc.gov.cn/diaochatongjisi/fileDir/resource/cms/2025/01/2025011418090142647.xlsx",
    2023:"https://www.pbc.gov.cn/diaochatongjisi/fileDir/resource/cms/2024/01/2024011714335855490.xlsx",
    2022:"https://www.pbc.gov.cn/diaochatongjisi/fileDir/resource/cms/2023/01/2023011817033232167.xls",
    2021:"https://www.pbc.gov.cn/diaochatongjisi/fileDir/resource/cms/2022/01/2022011916025645374.xlsx",
    2020:"https://www.pbc.gov.cn/diaochatongjisi/fileDir/resource/cms/2021/01/2021011909524873996.xls",
    2019:"https://www.pbc.gov.cn/diaochatongjisi/fileDir/resource/cms/2020/01/2020011915353816215.xls",
    2018:"https://www.pbc.gov.cn/diaochatongjisi/fileDir/resource/cms/2019/02/2019020115394298232.xls",
    2017:"https://www.pbc.gov.cn/diaochatongjisi/fileDir/resource/cms/2019/03/2019032816071149486.xls"
}

def get_file(url):

    conex = requests.get(url)

    if conex.status_code == 200:
        print("Success")
    else:
        print(f"status error: {conex.status_code}")

    if url[-3:] == "xls":
        data = pd.read_excel(BytesIO(conex.content), engine="xlrd")
    elif url[-4:] == "xlsx":
        data = pd.read_excel(BytesIO(conex.content))
    else:
        print("Format error")


    return data

datas_china = []
PATHS = []

for time in range(2025,2016,-1):
    a = get_file(file[time])

    datas_china.append(a)

BASE_DIR = Path(__file__).resolve().parents[1]
BRONZE_PATH = BASE_DIR / "Data" / "Bronze" / "M2_cn.json"

with open(BRONZE_PATH, "w", encoding="utf-8") as f:
    json.dump(
        [df.to_dict(orient="records") for df in datas_china],
        f,
        ensure_ascii=False
    )