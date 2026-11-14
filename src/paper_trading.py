class PaperPortfolio:
    """In-memory paper trading ledger. Resets when the server restarts."""
    def __init__(self, starting_cash=100000.0):
        self.starting_cash = float(starting_cash)
        self.cash = float(starting_cash)
        self.positions = {}
        self.orders = []

    def place_order(self, ticker, side, quantity, price):
        if not ticker or side not in ("BUY", "SELL"):
            raise ValueError("Provide a ticker and BUY or SELL side.")
        if quantity <= 0 or price <= 0:
            raise ValueError("Quantity and price must be greater than zero.")
        cost = quantity * price
        current = self.positions.get(ticker, 0.0)
        if side == "BUY":
            if cost > self.cash:
                raise ValueError("Insufficient paper cash.")
            self.cash -= cost
            self.positions[ticker] = current + quantity
        else:
            if quantity > current:
                raise ValueError("Not enough shares in this paper portfolio.")
            self.cash += cost
            self.positions[ticker] = current - quantity
        order = {"ticker": ticker, "side": side, "quantity": quantity, "price": price}
        self.orders.insert(0, order)
        return {"message": "Paper order completed.", "order": order, **self.summary()}

    def summary(self):
        return {"starting_cash": round(self.starting_cash, 2), "cash": round(self.cash, 2),
                "positions": {k: round(v, 4) for k, v in self.positions.items() if v > 0},
                "recent_orders": self.orders[:10]}
