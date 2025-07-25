def generate_forecast_summary(stock_name, forecast_df, rsi):
    last_row = forecast_df.tail(1).iloc[0]
    predicted_price = round(last_row["yhat"], 2)
    lower_bound = round(last_row["yhat_lower"], 2)
    upper_bound = round(last_row["yhat_upper"], 2)

    # Determine RSI-based trend sentiment
    if rsi > 70:
        rsi_trend = "Overbought"
        recommendation = "Consider waiting for a potential price correction before entering."
    elif rsi < 30:
        rsi_trend = "Oversold"
        recommendation = "This may present a buying opportunity if fundamentals align."
    else:
        rsi_trend = "Neutral"
        recommendation = "Wait for further confirmation before making a move."

    # Compose summary
    summary = (
        f"**Forecast Summary for {stock_name.upper()}**\n\n"
        f"- Projected Price in Forecast Period: ₹{predicted_price}\n"
        f"- Confidence Range: ₹{lower_bound} - ₹{upper_bound}\n"
        f"- RSI Status: {rsi_trend} (RSI = {rsi:.2f})\n\n"
        f"**Outlook:** Based on historical trends, the forecast indicates a likely price movement "
        f"towards ₹{predicted_price} within the selected horizon. The RSI suggests a {rsi_trend.lower()} condition.\n\n"
        f"**Strategy Recommendation:** {recommendation}\n\n"
        f"*Note: This insight is derived from historical price action and does not account for current news or events.*"
    )

    return summary
