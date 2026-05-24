import requests
from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime, timedelta
from config import Config
from services.official_rates import get_official_rate
from services.market_rates import get_usd_sdg_rate

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)