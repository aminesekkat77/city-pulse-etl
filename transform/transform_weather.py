import json
import pandas as pd
from pathlib import Path
from datetime import datetime

RAW_PATH = Path("raw_data/weather")
OUT_DIR = Path("transform/output/weather")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def transform_weather_file(file_path: Path, city_expected: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {
        "city": city_expected,  # ✅ on force la ville attendue
        "datetime": datetime.fromtimestamp(data.get("dt") or 0),
        "temp": (data.get("main") or {}).get("temp"),
        "humidity": (data.get("main") or {}).get("humidity"),
        "wind_speed": (data.get("wind") or {}).get("speed"),
        "weather": (data.get("weather") or [{}])[0].get("description"),
    }

def main():
    files = sorted(RAW_PATH.glob("*.json"))

    if not files:
        raise FileNotFoundError("Aucun fichier JSON weather trouvé dans raw_data/weather")

    records = []
    for fp in files:
        city_expected = fp.stem.split("_")[1]  
        records.append(transform_weather_file(fp, city_expected))

    df = pd.DataFrame(records).dropna()

    out_file = OUT_DIR / "weather_clean.csv"
    df.to_csv(out_file, index=False)
    print(f"[OK] weather_clean.csv créé : {out_file} (rows={len(df)})")

if __name__ == "__main__":
    main()
