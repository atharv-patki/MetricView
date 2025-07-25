import pandas as pd

# ---------- SALES KPI CALCULATIONS ---------- #

def calculate_sales_kpis(df: pd.DataFrame) -> dict:
    try:
        df = df.copy()

        total_revenue = df["Revenue"].sum() if "Revenue" in df.columns else 0
        avg_order_value = df["OrderValue"].mean() if "OrderValue" in df.columns else 0

        if "Leads" in df.columns and "WonDeals" in df.columns:
            conversion_rate = (df["WonDeals"].sum() / df["Leads"].sum()) * 100
        else:
            conversion_rate = 0

        if "LeadTime" in df.columns:
            avg_lead_time = df["LeadTime"].mean()
        else:
            avg_lead_time = 0

        return {
            "Total Revenue": round(total_revenue, 2),
            "Avg Order Value": round(avg_order_value, 2),
            "Conversion Rate (%)": round(conversion_rate, 2),
            "Avg Lead Time (Days)": round(avg_lead_time, 2)
        }

    except Exception as e:
        raise RuntimeError(f"Sales KPI calculation failed: {e}")


# ---------- EMPLOYEE KPI CALCULATIONS ---------- #

def calculate_employee_kpis(df: pd.DataFrame) -> dict:
    try:
        df = df.copy()

        tasks_done = df["TasksDone"].sum() if "TasksDone" in df.columns else 0
        bugs_resolved = df["BugsResolved"].sum() if "BugsResolved" in df.columns else 0
        avg_productivity = df["Productivity"].mean() if "Productivity" in df.columns else 0
        avg_attendance = df["Attendance"].mean() if "Attendance" in df.columns else 0

        return {
            "Total Tasks Done": int(tasks_done),
            "Bugs Resolved": int(bugs_resolved),
            "Avg Productivity (%)": round(avg_productivity, 2),
            "Avg Attendance (%)": round(avg_attendance, 2)
        }

    except Exception as e:
        raise RuntimeError(f"Employee KPI calculation failed: {e}")


# ---------- STOCK KPI CALCULATIONS ---------- #

def calculate_stock_kpis(df: pd.DataFrame) -> dict:
    try:
        df = df.copy()

        # Calculate Moving Averages
        df["MA50"] = df["Close"].rolling(window=50).mean()
        df["MA200"] = df["Close"].rolling(window=200).mean()

        # Calculate RSI (Relative Strength Index)
        delta = df["Close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        df["RSI"] = 100 - (100 / (1 + rs))

        # Drop rows with NaN values caused by rolling calculations
        df.dropna(inplace=True)

        price_change_pct = ((df["Close"].iloc[-1] - df["Close"].iloc[0]) / df["Close"].iloc[0]) * 100

        return {
            "Price Change (%)": round(price_change_pct, 2),
            "MA50": round(df["MA50"].iloc[-1], 2),
            "MA200": round(df["MA200"].iloc[-1], 2),
            "RSI": round(df["RSI"].iloc[-1], 2),
            "Volatility": round(df["Close"].pct_change().std() * 100, 2),
            "Volume": int(df["Volume"].iloc[-1])
        }

    except Exception as e:
        raise RuntimeError(f"Stock KPI calculation failed: {e}")
