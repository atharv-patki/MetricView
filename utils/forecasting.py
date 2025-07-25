from prophet import Prophet
import pandas as pd

def forecast_stock_prices(df, days_ahead=7):
    prophet_df = df[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})
    model = Prophet()
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=days_ahead)
    forecast = model.predict(future)

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], model.plot(forecast)
