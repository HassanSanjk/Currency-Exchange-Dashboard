import time
from flask import current_app
import requests

from redis_client import get_cached_rate, get_last_updated, save_rate
from services.history import save_snapshot as history_snapshot

URL = "https://api.currencyapi.com/v3/latest"


def get_official_rate(base, target):
    base = base.upper().strip()
    target = target.upper().strip()

    cached = get_cached_rate(base, target, "official")
    if cached is not None:
        return {
            "rate": cached,
            "status": "Cached",
            "updated_at": get_last_updated(base, target, "official"),
        }

    api_key = current_app.config["CURRENCYAPI_KEY"]
    if not api_key:
        raise ValueError("Missing CURRENCYAPI_KEY.")

    params = {
        "base_currency": base,
        "currencies": target,
    }

    headers = {
        "apikey": api_key,
    }

    start = time.perf_counter()
    response = requests.get(URL, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()
    elapsed = time.perf_counter() - start
    print(f"[TIMING] CurrencyAPI live fetch ({base}->{target}) took {elapsed:.4f}s")

    if "data" not in data or target not in data["data"]:
        raise ValueError("Invalid currency code or API response.")

    rate = float(data["data"][target]["value"])
    save_rate(base, target, "official", rate, max_age_hours=24)
    history_snapshot(base, target, "official", rate)

    return {
        "rate": rate,
        "status": "Live",
        "updated_at": get_last_updated(base, target, "official"),
    }