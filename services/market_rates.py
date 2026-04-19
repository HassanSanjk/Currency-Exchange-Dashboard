import requests
from bs4 import BeautifulSoup
from flask import current_app

from db import get_cached_rate, get_last_updated, save_rate
from services.official_rates import get_official_rate


def get_usd_sdg_rate():
    cached = get_cached_rate("USD", "SDG", "market", max_age_hours=6)
    if cached is not None:
        return {
            "rate": cached,
            "status": "Cached",
            "updated_at": get_last_updated("USD", "SDG", "market"),
        }

    rate = scrape_alsoug_usd_sdg_rate()
    save_rate("USD", "SDG", "market", rate)

    return {
        "rate": rate,
        "status": "Live",
        "updated_at": get_last_updated("USD", "SDG", "market"),
    }


def scrape_alsoug_usd_sdg_rate():
    url = current_app.config.get("ALSOUG_URL")
    if not url:
        raise ValueError("ALSOUG_URL is missing.")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    banks = soup.select("#currencies .bank")

    if not banks:
        raise ValueError("Currency blocks not found on Alsoug page.")

    fallback_rate = None

    for bank in banks:
        name_tag = bank.select_one(".bank-name")
        price_tag = bank.select_one(".bank-price.usd")

        if not price_tag:
            continue

        price_text = price_tag.text.strip().replace(",", "")

        try:
            price = float(price_text)
        except ValueError:
            continue

        if fallback_rate is None:
            fallback_rate = price

        if name_tag and "البديل" in name_tag.text.strip():
            return price

    if fallback_rate is not None:
        return fallback_rate

    raise ValueError("Could not extract USD/SDG market rate from Alsoug page.")
