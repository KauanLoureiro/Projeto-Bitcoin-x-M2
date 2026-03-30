import json

def load_m2_eu_bronze(data):

    with open("/opt/airflow/data/Bronze/M2_eu.json", "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )
