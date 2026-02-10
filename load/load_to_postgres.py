import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "city_pulse")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

BASE_DIR = Path(__file__).resolve().parents[1]
BIKES_CSV = BASE_DIR / "transform" / "output" / "bikes" / "bikes_clean.csv"
WEATHER_CSV = BASE_DIR / "transform" / "output" / "weather" / "weather_clean.csv"


def main():
    url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(url)

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE bikes_analytics;"))
        conn.execute(text("TRUNCATE TABLE weather_analytics;"))

    bikes_df = pd.read_csv(BIKES_CSV)
    weather_df = pd.read_csv(WEATHER_CSV)

    bikes_df.to_sql("bikes_analytics", engine, if_exists="append", index=False)
    weather_df.to_sql("weather_analytics", engine, if_exists="append", index=False)

    print(
        f"[OK] Load terminé : bikes_analytics + weather_analytics "
        f"(bikes={len(bikes_df)}, weather={len(weather_df)})"
    )


if __name__ == "__main__":
    main()
