import pandas as pd
from utils.stock_data import fetch_stock_data

def calculate_portfolio_metrics(portfolio):
    results = []
    for stock in portfolio:
        df = fetch_stock_data(stock["ticker"])
        if df.empty:
            continue
        latest_price = df["Close"].iloc[-1]
        total_value = latest_price * stock["quantity"]
        total_cost = stock["buy_price"] * stock["quantity"]
        profit = total_value - total_cost
        return_pct = ((latest_price - stock["buy_price"]) / stock["buy_price"]) * 100

        results.append({
            "Ticker": stock["ticker"].upper(),
            "Quantity": stock["quantity"],
            "Buy Price": stock["buy_price"],
            "Current Price": round(latest_price, 2),
            "Total Value": round(total_value, 2),
            "Total Gain/Loss": round(profit, 2),
            "Return (%)": round(return_pct, 2)
        })
    return pd.DataFrame(results)
