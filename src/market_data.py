
"""Indian NSE market data adapter using Yahoo Finance."""
from datetime import datetime, timezone

try:
    import yfinance as yf
except ImportError:
    yf = None


def normalize_ticker(ticker):
    ticker = ticker.strip().upper()
    if not ticker:
        raise ValueError("Please enter a stock symbol.")
    if "." not in ticker:
        ticker += ".NS"
    return ticker


def get_quote(ticker):
    ticker = normalize_ticker(ticker)

    if yf is None:
        return {"error": "yfinance is not installed."}

    try:
        hist = yf.Ticker(ticker).history(
            period="5d", interval="1d", auto_adjust=True
        )

        if hist.empty:
            return {"error": f"No live data available for {ticker}."}

        latest = float(hist["Close"].iloc[-1])
        previous = (
            float(hist["Close"].iloc[-2])
            if len(hist) > 1 else latest
        )
        change = latest - previous

        return {
            "ticker": ticker,
            "price": round(latest, 2),
            "change": round(change, 2),
            "change_pct": round(
                change / previous * 100, 2
            ) if previous else 0,
            "currency": "INR",
            "source": "Yahoo Finance",
            "as_of": str(hist.index[-1]),
            "demo": False
        }

    except Exception as exc:
        return {"error": f"Unable to fetch live data: {exc}"}


def get_history(ticker, period="1mo"):
    ticker = normalize_ticker(ticker)

    if yf is None:
        return []

    try:
        hist = yf.Ticker(ticker).history(
            period=period, interval="1d", auto_adjust=True
        )

        if hist.empty:
            return []

        return [
            {
                "date": idx.strftime("%Y-%m-%d"),
                "close": round(float(row["Close"]), 2),
                "volume": int(row.get("Volume", 0))
            }
            for idx, row in hist.iterrows()
        ]

    except Exception:
        return []
