# SPY Trading Agent

A modular Flask dashboard for monitoring SPY and other tickers, reviewing historical price data and descriptive technical indicators, and practicing with a paper-trading ledger.

## Features
- Stock quote and historical chart (Yahoo Finance through `yfinance`)
- Percentage-change monitoring
- 5-day and 20-day simple moving averages
- Paper trading simulator (no broker connection; no real orders)
- Demo-data fallback when the market-data provider is unavailable
- Modular Flask structure and responsive dashboard

> This application does not predict stock prices and does not provide investment advice. Market data can be delayed or unavailable. The paper portfolio is stored in memory and resets when the server restarts.

## Run on Windows
```powershell
py -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Run on macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

## Project structure
```text
SPY_Trading_Agent/
├── app.py
├── src/
│   ├── __init__.py
│   ├── market_data.py
│   ├── analysis.py
│   └── paper_trading.py
├── templates/
│   └── index.html
├── static/
│   ├── css/style.css
│   └── js/app.js
├── requirements.txt
└── README.md
```

## Notes
- The dashboard uses Yahoo Finance via `yfinance` when available.
- If live retrieval fails, the app shows clearly labeled deterministic demo data.
- Paper-trading orders are simulated only and are not sent to a broker.
