import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker: str) -> pd.DataFrame:
    try:
        df = yf.download(ticker, period="6mo", interval="1d", progress=False, auto_adjust=False)

        if df.empty:
            raise ValueError("No data returned for the given ticker")

        df.reset_index(inplace=True)

        # 🔧 Flatten MultiIndex if needed
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        else:
            df.columns = [col.split()[-1] if " " in col else col for col in df.columns]

        # ✅ Log raw columns
        print("✅ Cleaned Columns:", df.columns.tolist())

        # 🔥 Drop duplicate 'Close' columns, keep the first
        seen = set()
        new_cols = []
        for col in df.columns:
            if col in seen and col in ["Close", "Open", "High", "Low", "Volume"]:
                continue
            seen.add(col)
            new_cols.append(col)
        df = df[new_cols]

        # 🧪 Ensure required columns exist
        required_cols = {"Date", "Close", "Volume"}
        if not required_cols.issubset(df.columns):
            raise ValueError("Missing required stock columns after flattening")

        # === Derived KPIs ===
        df["MA5"] = df["Close"].rolling(window=5).mean()
        df["MA20"] = df["Close"].rolling(window=20).mean()
        df["% Change"] = df["Close"].pct_change() * 100
        df["Volatility"] = df["Close"].rolling(window=5).std()
        df["RSI"] = compute_rsi(df["Close"])

        return df.dropna()

    except Exception as e:
        raise RuntimeError(f"Error fetching stock data: {e}")

def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / (avg_loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))

    return rsi
