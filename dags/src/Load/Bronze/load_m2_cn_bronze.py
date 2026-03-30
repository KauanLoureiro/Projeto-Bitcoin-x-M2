import json

def load_m2_cn_bronze(data):

    with open("/opt/airflow/data/Bronze/M2_cn.json", "w", encoding="utf-8") as f:
        json.dump(
            [df.to_dict(orient="records") for df in data],
            f,
            ensure_ascii=False
        )
