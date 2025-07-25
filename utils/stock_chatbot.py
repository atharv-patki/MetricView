import re
from utils.stock_data import fetch_stock_data

# List of common words we don’t want to mistake for tickers
COMMON_WORDS = {
    "WHAT", "IS", "THE", "OF", "SHOW", "ME", "A", "AN", "TO", "FOR", "ON", "BY", "AND", "PLEASE",
    "PRICE", "VALUE", "RSI", "VOLATILITY", "MA5", "MA20", "SUMMARY", "ABOUT"
}

def extract_ticker(query):
    words = re.findall(r'\b[A-Z]{2,10}(?:\.NS)?\b', query.upper())
    for word in words:
        if word not in COMMON_WORDS:
            return word
    return None

def generate_stock_response(query, df_default, default_ticker):
    query = query.lower()

    # Greetings
    if any(greet in query for greet in ["hello", "hi", "hey"]):
        return "Hello! 👋 How can I assist you with stock data today?"
    elif "bye" in query or "goodbye" in query:
        return "Goodbye! 👋 Feel free to return anytime for stock updates."
    elif "thank" in query:
        return "You're welcome! 😊 Let me know if you have more questions."

    # Detect custom ticker
    ticker = extract_ticker(query) or default_ticker
    try:
        if ticker != default_ticker:
            df = fetch_stock_data(ticker)
            df = df.dropna(subset=["Close", "RSI", "Volatility", "MA5", "MA20"])
        else:
            df = df_default

        latest = df.iloc[-1]

        if "price" in query:
            return f"The latest closing price of {ticker.upper()} is ₹{latest['Close']:.2f}."
        elif "rsi" in query:
            return f"The current RSI of {ticker.upper()} is {latest['RSI']:.2f}."
        elif "volatility" in query:
            return f"The volatility of {ticker.upper()} is {latest['Volatility']:.2f}."
        elif "ma5" in query:
            return f"MA5 (5-day moving average) is {latest['MA5']:.2f}."
        elif "ma20" in query:
            return f"MA20 (20-day moving average) is {latest['MA20']:.2f}."
        elif "summary" in query or ("about" in query and ticker.lower() in query):
            return (
                f"{ticker.upper()} is currently priced at ₹{latest['Close']:.2f}, "
                f"RSI: {latest['RSI']:.2f}, Volatility: {latest['Volatility']:.2f}, "
                f"MA5: {latest['MA5']:.2f}, MA20: {latest['MA20']:.2f}."
            )
        else:
            return "❓ I'm not sure how to answer that. Try asking about price, RSI, MA5, or summary."

    except Exception as e:
        return f"⚠️ Could not fetch data for {ticker.upper()}. Please make sure the ticker is valid."
