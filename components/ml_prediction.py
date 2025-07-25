import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# --- Step 1: Get historical stock data ---
def get_stock_data(ticker):
    df = yf.download(ticker, period="6mo", interval="1d", auto_adjust=True)
    df.dropna(inplace=True)
    return df

# --- Step 2: Train ML model ---
def train_model(df):
    df["Price_Change"] = df["Close"].pct_change()
    df["Target"] = df["Price_Change"].shift(-1)
    df.dropna(inplace=True)

    # Target class: 1 = Buy, -1 = Sell, 0 = Hold
    df["Target"] = df["Target"].apply(lambda x: 1 if x > 0.01 else (-1 if x < -0.01 else 0))

    X = df[["Open", "High", "Low", "Close", "Volume"]]
    y = df["Target"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)

    return model, scaler

# --- Step 3A: Predict action for owned stock ---
def predict_owned_stock(ticker, buy_price):
    df = get_stock_data(ticker)
    
    if df.empty or "Close" not in df.columns:
        return "Error: Stock data unavailable or malformed."

    current_price = df["Close"].iloc[-1]

    try:
        buy_price = float(buy_price)
    except:
        return "Error: Invalid buy price."

    # Ensure current_price is scalar
    if isinstance(current_price, pd.Series):
        current_price = current_price.iloc[-1]

    if float(current_price) > (buy_price * 1.05):
        return "Sell (Profit zone)"
    elif float(current_price) < (buy_price * 0.95):
        return "Buy / Hold (Stock undervalued)"
    else:
        return "Hold (Near your buy price)"

# --- Step 3B: Predict market action with volatility ---
def predict_market_action(ticker):
    df = get_stock_data(ticker)
    model, scaler = train_model(df)

    latest = df[["Open", "High", "Low", "Close", "Volume"]].iloc[-1:]
    latest_scaled = scaler.transform(latest)
    prediction = model.predict(latest_scaled)[0]

    # Volatility check
    df["Volatility"] = df["High"] - df["Low"]
    recent_volatility = df["Volatility"].rolling(window=5).mean().iloc[-1]
    avg_volatility = df["Volatility"].mean()

    if prediction == 1:
        return "Buy"
    elif prediction == -1:
        return "Sell"
    else:
        if recent_volatility > avg_volatility * 1.2:
            return "Wait before Buying (High Volatility)"
        return "Hold"

