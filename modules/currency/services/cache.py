import json
from pathlib import Path
from datetime import date

CACHE_FILE = Path("rates_cache.json")

def load_cache():
    if not CACHE_FILE.exists():
        return {}
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_cache(rates: dict):
    today = date.today().isoformat()  
    data = {
        "date": today,
        "rates": rates
    }
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
