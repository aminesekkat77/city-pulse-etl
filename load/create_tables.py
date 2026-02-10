import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "city_pulse")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

BASE_DIR = Path(__file__).resolve().parents[1]   # => /opt/airflow/dags

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
SQL_FILE = BASE_DIR / "load" / "create_tables.sql"


def main():
    url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(url) 

    with open(SQL_FILE, "r", encoding="utf-8") as f:
        sql = f.read()  

    with engine.begin() as conn:
        conn.execute(text(sql))

    print("[OK] Tables créées / mises à jour via create_tables.sql")

if __name__ == "__main__":
    main()
