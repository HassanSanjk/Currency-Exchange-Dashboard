import json
import time
import requests
from flask import Flask, current_app, request, jsonify, send_from_directory
from datetime import datetime, timedelta
from config import Config
from redis_client import get_redis_client
from services.official_rates import get_official_rate
from services.market_rates import get_usd_sdg_rate
from services.history import get_history

START_TIME = time.time()

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def index():
    return send_from_directory("static/react", "index.html")


@app.route("/convert", methods=["POST"])
def convert():
    base = request.form["base"].upper().strip()
    target = request.form["target"].upper().strip()
    amount_text = request.form["amount"].strip()

    error = None
    official_data = None
    market_data = None

    try:
        amount = float(amount_text)

        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        # Official / API conversion
        off = get_official_rate(base, target)
        rate = off["rate"]
        converted = amount * rate
        utc_time = datetime.strptime(off["updated_at"], "%Y-%m-%d %H:%M:%S")
        myt_time = utc_time + timedelta(hours=8)

        official_data = {
            "base": base,
            "target": target,
            "amount": amount,
            "converted": converted,
            "rate": rate,
            "status": off["status"],
            "updated": utc_time.strftime("%H:%M"),
            "updatedMyt": myt_time.strftime("%H:%M"),
        }

        # SDG market conversion
        if base == "SDG" or target == "SDG":
            mkt = get_usd_sdg_rate()
            usd_sdg = mkt["rate"]
            utc_time_m = datetime.strptime(mkt["updated_at"], "%Y-%m-%d %H:%M:%S")
            myt_time_m = utc_time_m + timedelta(hours=8)

            market_data = {
                "base": base,
                "target": target,
                "amount": amount,
                "ref": usd_sdg,
                "status": mkt["status"],
                "updated": utc_time_m.strftime("%H:%M"),
                "updatedMyt": myt_time_m.strftime("%H:%M"),
            }

            if base == "USD" and target == "SDG":
                market_data["rate"] = usd_sdg
                market_data["converted"] = amount * usd_sdg

            elif base == "SDG" and target == "USD":
                market_data["rate"] = 1 / usd_sdg
                market_data["converted"] = amount * market_data["rate"]

            elif base == "SDG":
                usd_to_target = get_official_rate("USD", target)["rate"]
                market_data["rate"] = (1 / usd_sdg) * usd_to_target
                market_data["converted"] = amount * market_data["rate"]

            elif target == "SDG":
                base_to_usd = get_official_rate(base, "USD")["rate"]
                market_data["rate"] = base_to_usd * usd_sdg
                market_data["converted"] = amount * market_data["rate"]

    except ValueError as e:
        error = str(e)
    except requests.exceptions.RequestException as e:
        error = f"Request failed: {e}"
    except Exception as e:
        error = f"Something went wrong: {e}"

    return jsonify({"error": error, "official": official_data, "market": market_data})


@app.route("/api/history", methods=["GET"])
def api_history():
    base = request.args.get("base", "USD").upper().strip()
    target = request.args.get("target", "SDG").upper().strip()
    official = get_history(base, target, "official")
    market = get_history("USD", "SDG", "market") if "SDG" in (base, target) else []
    return jsonify({"official": official, "market": market})


CURRENCIES_API_URL = "https://api.currencyapi.com/v3/currencies"

FLAG_OVERRIDES = {
    "USD": "us", "EUR": "eu", "GBP": "gb", "JPY": "jp", "CHF": "ch",
    "CAD": "ca", "AUD": "au", "NZD": "nz", "CNY": "cn", "INR": "in",
    "KRW": "kr", "BRL": "br", "RUB": "ru", "MXN": "mx", "SEK": "se",
    "NOK": "no", "DKK": "dk", "ZAR": "za", "TRY": "tr", "AED": "ae",
    "SAR": "sa", "EGP": "eg", "NGN": "ng", "HKD": "hk", "SGD": "sg",
    "MYR": "my", "THB": "th", "ILS": "il", "PLN": "pl", "ARS": "ar",
}


@app.route("/api/currencies", methods=["GET"])
def api_currencies():
    client = get_redis_client()
    cached = client.get("currencies:v2")
    if cached:
        return jsonify({"currencies": json.loads(cached.decode("utf-8"))})

    api_key = current_app.config["CURRENCYAPI_KEY"]
    if not api_key:
        return jsonify({"error": "Missing CURRENCYAPI_KEY"}), 500

    headers = {"apikey": api_key}
    response = requests.get(CURRENCIES_API_URL, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()

    currencies = [
        {
            "code": c["code"],
            "name": c["name"],
            "symbol": c.get("symbol", ""),
            "flag_country": FLAG_OVERRIDES.get(c["code"]) or (c.get("countries", [None])[0].lower() if c.get("countries") else None),
        }
        for c in data.get("data", {}).values()
    ]
    currencies.sort(key=lambda x: x["code"])

    client.setex("currencies:v2", 2592000, json.dumps(currencies))

    return jsonify({"currencies": currencies})


@app.route("/health", methods=["GET"])
def health():
    redis_ok = False
    last_fetch = {"currencyapi": None, "alsoug": None}
    try:
        client = get_redis_client()
        redis_ok = client.ping()
        caf = client.get("rate:USD:SDG:official:updated")
        alf = client.get("rate:USD:SDG:market:updated")
        if caf:
            last_fetch["currencyapi"] = caf.decode("utf-8")
        if alf:
            last_fetch["alsoug"] = alf.decode("utf-8")
    except Exception:
        redis_ok = False
    return jsonify({
        "status": "ok" if redis_ok else "degraded",
        "redis": redis_ok,
        "uptime_seconds": int(time.time() - START_TIME),
        "last_fetch": last_fetch,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)