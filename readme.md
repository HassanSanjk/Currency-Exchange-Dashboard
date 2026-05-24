# Currency Exchange Dashboard

A currency converter that gives you **both** official exchange rates and real Sudan parallel market rates (because the official SDG rate and what people actually pay on the street can be very different).

Built as a learning project — React frontend, Flask API, Redis caching, all wrapped in Docker and deployed on AWS.

---

## Live Demo

https://currency-app.duckdns.org

---

## What It Does

- Convert between any two currencies using official API rates
- If SDG (Sudanese Pound) is involved, it also shows the **parallel market rate** scraped from Alsoug.com
- Uses USD as a bridge for cross-currency conversions (e.g. EUR → SDG)
- Caches results in Redis so it doesn't hit the API every single time
- Shows you whether each rate is "Live" (freshly fetched) or "Cached" (from the last request)

---

## Tech Stack

- **Frontend:** React (Vite)
- **Backend:** Python (Flask + Gunicorn)
- **Cache:** Redis
- **Container:** Docker + docker-compose
- **Deployment:** AWS EC2 (Ubuntu, free tier)

---

## Project Structure

```
curency convertor/
├── app.py                  # Flask app (JSON API)
├── config.py               # Environment variables
├── redis_client.py         # Redis caching functions
├── services/
│   ├── official_rates.py   # Fetches from CurrencyAPI
│   └── market_rates.py     # Scrapes Alsoug for SDG rate
├── frontend/               # React source code
│   └── src/
│       ├── App.jsx
│       ├── CurrencyForm.jsx
│       ├── OfficialResult.jsx
│       ├── MarketResult.jsx
│       └── ErrorBanner.jsx
├── static/react/           # Built React files (served by Flask)
├── Dockerfile
├── docker-compose.yml
└── .env                    # Your API keys (not committed)
```

---

## How It Works (Simple Version)

1. You type in a currency pair (e.g. USD → SDG) and an amount
2. Flask checks Redis: "do I already have this rate cached?"
3. If yes → returns the cached rate (faster, no API call)
4. If no → fetches from CurrencyAPI (or scrapes Alsoug for SDG), saves it in Redis, returns it
5. Redis auto-deletes old entries after 24 hours (official) or 6 hours (market)

---

## Run It Locally (Without Docker)

### 1. Prerequisites
- Python 3.12+
- Redis running on your machine (or use Docker for Redis only)

### 2. Clone and set up

```bash
git clone <repo-url>
cd "curency convertor"
pip install -r requirements.txt
```

### 3. Create a `.env` file

```
SECRET_KEY=your_secret_key
CURRENCYAPI_KEY=your_api_key_here
ALSOUG_URL=https://www.alsoug.com
REDIS_URL=redis://localhost:6379/0
```

> You can get a free API key from https://currencyapi.com

### 4. Build the React frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

### 5. Run the app

```bash
python app.py
```

Visit **http://localhost:5000**

---

## Run It With Docker (Easier)

```bash
docker compose up --build -d
```

This starts both the Flask app and Redis. Visit **http://localhost:5000**.

---

## Notes

- The parallel market rate comes from public listings on Alsoug — it's an estimate, not a guaranteed price
- Official API rates might not reflect the real street value of SDG
- Redis caches expire automatically (24h official, 6h market)

## Things I Want to Add Later

- Historical rate chart
- Dark mode
- A proper CI/CD pipeline


