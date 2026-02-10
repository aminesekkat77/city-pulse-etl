import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CITIES = ["lyon", "toulouse"]
API_KEY = os.getenv("API_KEY_BIKES")
BASE_URL = "https://api.jcdecaux.com/vls/v1/stations"


def fetch_bike_data(city: str):
    params = {"contract": city, "apiKey": API_KEY}
    r = requests.get(BASE_URL, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def main():
    if not API_KEY:
        raise ValueError("API_KEY_BIKES manquante. Vérifie ton fichier .env")

    os.makedirs("raw_data/bikes", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    for city in CITIES:
        data = fetch_bike_data(city)
        out_file = f"raw_data/bikes/bikes_{city}_{ts}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
