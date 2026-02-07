import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "city_pulse")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

BIKES_CSV = "transform/output/bikes/bikes_clean.csv"
WEATHER_CSV = "transform/output/weather/weather_clean.csv"

def main():
    url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(url)

    with engine.connect() as conn:
        conn.execute(text("SELECT 1;"))

    bikes_df = pd.read_csv(BIKES_CSV)
    bikes_df.to_sql("bikes_analytics", engine, if_exists="replace", index=False)

    weather_df = pd.read_csv(WEATHER_CSV)
    weather_df.to_sql("weather_analytics", engine, if_exists="replace", index=False)

if __name__ == "__main__":
    main()
