import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CITIES = ["Lyon", "Toulouse"]
API_KEY = os.getenv("API_KEY_WEATHER")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city: str):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    r = requests.get(BASE_URL, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def main():
    if not API_KEY:
        raise ValueError("API_KEY_WEATHER manquante. Vérifie ton fichier .env")

    os.makedirs("raw_data/weather", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    for city in CITIES:
        data = fetch_weather(city)
        out_file = f"raw_data/weather/weather_{city}_{ts}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
