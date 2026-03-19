#%%
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / "Environment" / ".env"

load_dotenv(dotenv_path=ENV_PATH)

def con():
    conn = psycopg2.connect(
        host=os.getenv("host"),
        dbname=os.getenv("dbname"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        port=os.getenv("port")
    )
    return conn
