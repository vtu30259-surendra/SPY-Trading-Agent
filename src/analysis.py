def calculate_indicators(rows):
    closes = [float(x["close"]) for x in rows if x.get("close") is not None]
    if not closes:
        return {"message": "No historical data available."}
    def sma(n):
        return round(sum(closes[-n:]) / min(n, len(closes)), 2)
    first, last = closes[0], closes[-1]
    return {
        "latest_close": round(last, 2),
        "period_change_pct": round(((last-first)/first)*100, 2) if first else 0,
        "sma_5": sma(5), "sma_20": sma(20),
        "data_points": len(closes),
        "note": "Descriptive indicators only; this application does not predict future prices."
    }
