import requests
from flask import Flask, render_template, request

from config import Config
from services.official_rates import get_official_rate
from services.market_rates import get_usd_sdg_rate

app = Flask(__name__)
app.config.from_object(Config)


def format_number(value):
    if value is None:
        return None
    return f"{value:,.3f}"


@app.route("/")
def index():
    return render_template(
        "currency.html",
        base="",
        target="",
        amount="",
        error=None,
        result=None,
        rate=None,
        official_status=None,
        official_updated=None,
        market_result=None,
        market_rate=None,
        market_ref=None,
        market_status=None,
        market_updated=None,
        show_market_note=False,
    )


@app.route("/convert", methods=["POST"])
def convert():
    base = request.form["base"].upper().strip()
    target = request.form["target"].upper().strip()
    amount_text = request.form["amount"].strip()

    error = None

    result = None
    rate = None
    official_status = None
    official_updated = None

    market_result = None
    market_rate = None
    market_ref = None
    market_status = None
    market_updated = None
    show_market_note = False

    try:
        amount = float(amount_text)

        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        # Official / API conversion
        official = get_official_rate(base, target)
        rate = official["rate"]
        result = amount * rate
        official_status = official["status"]
        official_updated = str(official["updated_at"])

        # SDG market conversion
        if base == "SDG" or target == "SDG":
            market = get_usd_sdg_rate()
            usd_sdg = market["rate"]

            market_ref = usd_sdg
            market_status = market["status"]
            market_updated = str(market["updated_at"])
            show_market_note = True

            if base == "USD" and target == "SDG":
                market_rate = usd_sdg
                market_result = amount * market_rate

            elif base == "SDG" and target == "USD":
                market_rate = 1 / usd_sdg
                market_result = amount * market_rate

            elif base == "SDG":
                usd_to_target = get_official_rate("USD", target)["rate"]
                market_rate = (1 / usd_sdg) * usd_to_target
                market_result = amount * market_rate

            elif target == "SDG":
                base_to_usd = get_official_rate(base, "USD")["rate"]
                market_rate = base_to_usd * usd_sdg
                market_result = amount * market_rate

    except ValueError as e:
        error = str(e)
    except requests.exceptions.RequestException as e:
        error = f"Request failed: {e}"
    except Exception as e:
        error = f"Something went wrong: {e}"

    return render_template(
        "currency.html",
        base=base,
        target=target,
        amount=amount_text,
        error=error,
        result=format_number(result),
        rate=format_number(rate),
        official_status=official_status,
        official_updated=official_updated,
        market_result=format_number(market_result),
        market_rate=format_number(market_rate),
        market_ref=format_number(market_ref),
        market_status=market_status,
        market_updated=market_updated,
        show_market_note=show_market_note,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)