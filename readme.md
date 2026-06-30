# Currency Exchange Dashboard

A currency converter that shows both official exchange rates and the Sudan parallel market rate. The official SDG rate and what people actually pay on the street can be very different, so this gives you both.

React frontend, Flask API, Redis caching, Docker on AWS.

## Live Demo

https://currency-app.duckdns.org

## What It Does

- Convert between any two currencies using official API rates
- If SDG is involved, also shows the parallel market rate scraped from Alsoug.com
- Uses USD as a bridge for cross-currency conversions (e.g. EUR → SDG)
- Draws a chart comparing official vs market rates over time
- Caches everything in Redis so it doesn't hit the API every time
- Shows whether each rate is "Live" (freshly fetched) or "Cached" (from the last request)

## Tech Stack

- Frontend: React (Vite) + Recharts
- Backend: Python (Flask + Gunicorn)
- Cache: Redis
- Container: Docker + docker-compose
- Hosting: AWS EC2 free tier

## Project Structure

```
├── app.py                  # Flask app (JSON API)
├── config.py               # Environment variables
├── redis_client.py         # Redis caching functions
├── services/
│   ├── history.py          # Rate snapshots in Redis sorted sets
│   ├── official_rates.py   # Fetches from CurrencyAPI
│   └── market_rates.py     # Scrapes Alsoug for SDG rate
├── frontend/src/
│   ├── App.jsx
│   ├── CurrencyForm.jsx    # Dropdowns with flags
│   ├── HistoryChart.jsx    # Recharts dual-line chart
│   ├── OfficialResult.jsx
│   ├── MarketResult.jsx
│   └── ErrorBanner.jsx
├── static/react/           # Built frontend (served by Flask)
├── Dockerfile
├── docker-compose.yml
└── .env                    # API keys (not committed)
```

## API Endpoints

| Route | What it does |
|-------|-------------|
| `POST /convert` | Convert currencies, returns official + market rates |
| `GET /api/history?base=USD&target=SDG` | Rate snapshots for the last 30 days |
| `GET /api/currencies` | List of all supported currencies (cached 30 days) |
| `GET /health` | Redis status, uptime, last fetch times |

## Run It

### With Docker

```bash
docker compose up --build
```

Visit http://localhost:5000

### Without Docker

You need Python 3.12+, Redis, and Node.js.

```bash
pip install -r requirements.txt
cd frontend && npm install && npm run build && cd ..
python app.py
```

Create a `.env` file:

```
SECRET_KEY=your_secret_key
CURRENCYAPI_KEY=your_api_key_here
ALSOUG_URL=https://www.alsoug.com
REDIS_URL=redis://localhost:6379/0
```

Get a free API key from https://currencyapi.com

## How the History Chart Works

Every time a live rate is fetched (not cached), it saves a snapshot to a Redis sorted set. The chart fetches the last 30 days of snapshots and draws two lines — green for official rates, orange for the market rate. Alsoug rate is collected every 6 hours via cron. Official rates are saved whenever someone visits the site (no cron, because CurrencyAPI is 300 requests/month).

## Notes

- The parallel market rate comes from public listings on Alsoug — it's an estimate
- Official API rates don't reflect the real street value of SDG
- Redis caches expire: 24h for official rates, 6h for market rates

## Stuff I Might Add Later

- Dark mode
- A proper CI/CD pipeline
