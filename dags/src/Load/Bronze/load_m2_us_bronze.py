import json

def load_m2_us_bronze(data):
    with open("/opt/airflow/data/Bronze/M2_us.json", "w", encoding="utf-8") as f:
        json.dump(
            data, f
        )
