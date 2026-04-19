from flask import current_app
import requests

from db import get_cached_rate, get_last_updated, save_rate

URL = "https://api.currencyapi.com/v3/latest"


def get_official_rate(base, target):
    base = base.upper().strip()
    target = target.upper().strip()

    cached = get_cached_rate(base, target, "official", max_age_hours=24)
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

    response = requests.get(URL, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()

    if "data" not in data or target not in data["data"]:
        raise ValueError("Invalid currency code or API response.")

    rate = float(data["data"][target]["value"])
    save_rate(base, target, "official", rate)

    return {
        "rate": rate,
        "status": "Live",
        "updated_at": get_last_updated(base, target, "official"),
    }