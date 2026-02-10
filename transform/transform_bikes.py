import json
import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_PATH = BASE_DIR / "raw_data" / "bikes"
OUT_DIR = BASE_DIR / "transform" / "output" / "bikes"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def transform_bike_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        stations = json.load(f)

    records = []
    for st in stations:
        last_update = st.get("last_update")
        records.append({
            "city": st.get("contract_name"),
            "station_id": st.get("number"),
            "station_name": st.get("name"),
            "available_bikes": st.get("available_bikes"),
            "bike_stands": st.get("bike_stands"),
            "status": st.get("status"),
            "datetime": datetime.fromtimestamp(last_update / 1000) if last_update else None,
        })
    return records

def main():
    all_records = []
    files = sorted(RAW_PATH.glob("*.json"))

    if not files:
        raise FileNotFoundError("Aucun fichier JSON bikes trouvé dans raw_data/bikes")

    for fp in files:
        all_records.extend(transform_bike_file(fp))

    df = pd.DataFrame(all_records).dropna()
    out_file = OUT_DIR / "bikes_clean.csv"
    df.to_csv(out_file, index=False)

if __name__ == "__main__":
    main()
