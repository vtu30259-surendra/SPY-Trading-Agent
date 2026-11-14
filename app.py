from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from src.market_data import get_quote, get_history
from src.analysis import calculate_indicators
from src.paper_trading import PaperPortfolio

app = Flask(__name__)
portfolio = PaperPortfolio()

def local_time():
    try:
        return datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%d %b %Y, %I:%M %p IST")
    except ZoneInfoNotFoundError:
        return datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")

@app.route("/")
def dashboard():
    return render_template("index.html", timestamp=local_time())

@app.route("/api/quote/<ticker>")
def quote(ticker):
    data = get_quote(ticker.upper())
    if not data:
        return jsonify({"error": "No market data available for this ticker."}), 404
    return jsonify(data)

@app.route("/api/history/<ticker>")
def history(ticker):
    period = request.args.get("period", "1mo")
    rows = get_history(ticker.upper(), period)
    return jsonify(rows)

@app.route("/api/analysis/<ticker>")
def analysis(ticker):
    rows = get_history(ticker.upper(), "3mo")
    return jsonify(calculate_indicators(rows))

@app.route("/api/portfolio", methods=["GET", "POST"])
def paper_portfolio():
    if request.method == "POST":
        body = request.get_json(silent=True) or {}
        try:
            result = portfolio.place_order(
                ticker=str(body.get("ticker", "SPY")).upper(),
                side=str(body.get("side", "BUY")).upper(),
                quantity=float(body.get("quantity", 1)),
                price=float(body.get("price", 0))
            )
            return jsonify(result)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
    return jsonify(portfolio.summary())

@app.route("/health")
def health():
    return jsonify({"status": "ok", "time": local_time()})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
