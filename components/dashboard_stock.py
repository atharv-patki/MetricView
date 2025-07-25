import streamlit as st
import plotly.graph_objects as go
from utils.stock_data import fetch_stock_data
from datetime import datetime
from config.style_config import GAUGE_THRESHOLDS
from utils.layout_utils import create_gauge, bar_chart
import pandas as pd
from utils.stock_chatbot import generate_stock_response
from utils.feedback import save_feedback
from utils.forecasting import forecast_stock_prices
from utils.ai_summary import generate_forecast_summary
from utils.portfolio import calculate_portfolio_metrics
from utils.news_sentiment import fetch_market_news, analyze_sentiment
from components.ml_prediction import predict_market_action, predict_owned_stock

# === Helpers ===
def get_rsi_trend(rsi):
    if rsi > 70:
        return "Overbought"
    elif rsi < 30:
        return "Oversold"
    else:
        return "Neutral"

def line_chart_with_ma(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], mode="lines+markers", name="Close", line=dict(color="blue", width=2)))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["MA5"], mode="lines", name="MA5", line=dict(color="green", width=2, dash="dot")))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["MA20"], mode="lines", name="MA20", line=dict(color="orange", width=2, dash="dash")))

    fig.update_layout(
        title=dict(text="📈 CP vs MA", font=dict(size=20, color="#003566")),
        xaxis=dict(title="Date", tickfont=dict(color="#003566")),
        yaxis=dict(title="Price", tickfont=dict(color="#003566")),
        legend=dict(font=dict(color="#003566"), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(color="#003566"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=450,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# === Main Render Function ===
def render_stock_dashboard(ticker: str):
    with st.sidebar:
        st.markdown("### Feedback")
        if "show_feedback_box" not in st.session_state:
            st.session_state.show_feedback_box = False

        if st.button("Send Feedback"):
            st.session_state.show_feedback_box = True

        if st.session_state.show_feedback_box:
            feedback_input = st.text_area("Your feedback here...", key="feedback_input_sidebar")
            submit_col, cancel_col = st.columns([1, 1])
            with submit_col:
                if st.button("Submit", key="submit_sidebar"):
                    if feedback_input.strip():
                        save_feedback(feedback_input)
                        st.success("Thanks for your feedback!")
                        st.session_state.show_feedback_box = False
                    else:
                        st.warning("Please write something before submitting.")
            with cancel_col:
                if st.button("Cancel", key="cancel_sidebar"):
                    st.session_state.show_feedback_box = False

    st.header(f"Stock Dashboard: {ticker.upper()}")

    try:
        df = fetch_stock_data(ticker)
        df = df.loc[:, ~df.columns.duplicated()]
        if df.empty:
            st.warning("No data available for the given ticker.")
            return

        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")
        df = df.dropna(subset=["Close", "MA5", "MA20", "RSI", "Volatility"])

        latest = df.iloc[-1]
        price = float(latest["Close"])
        rsi = float(latest["RSI"])
        change = float(latest["% Change"])
        volatility = float(latest["Volatility"])
        ma5 = float(latest["MA5"])
        ma20 = float(latest["MA20"])

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Overview", "Chatbot", "Forecast & Insights","Portfolio Tracker","Market News & Sentiment","Prediction"])

        with tab1:
            with st.expander("Set Custom Alerts"):
                alert_kpi = st.selectbox("Choose KPI for Alert", ["RSI", "Volatility"])
                condition = st.radio("Condition", [">", "<"])
                threshold = st.number_input("Threshold Value", value=70.0 if alert_kpi == "RSI" else 2.0)

            st.subheader("Today's KPIs")
            col1, col2, col3 = st.columns(3)
            col1.metric("Price", f"₹{price:.2f}", f"{change:.2f}%")
            col2.metric("RSI", f"{rsi:.2f}", get_rsi_trend(rsi))
            col3.metric("Volatility", f"{volatility:.2f}", None)

            alert_value = rsi if alert_kpi == "RSI" else volatility
            if (condition == ">" and alert_value > threshold) or (condition == "<" and alert_value < threshold):
                st.warning(f"Alert: {alert_kpi} is {alert_value:.2f}, which is {condition} {threshold}")

            st.subheader("Performance Gauges")
            gauge_col1, gauge_col2, gauge_col3 = st.columns(3)
            with gauge_col1:
                rsi_range = GAUGE_THRESHOLDS["RSI"]
                st.plotly_chart(create_gauge("RSI", rsi, rsi_range["min"], rsi_range["max"]), use_container_width=True)
            with gauge_col2:
                st.plotly_chart(create_gauge("MA5", ma5, df["Close"].min(), df["Close"].max()), use_container_width=True)
            with gauge_col3:
                st.plotly_chart(create_gauge("MA20", ma20, df["Close"].min(), df["Close"].max()), use_container_width=True)

            st.subheader("Closing Price vs Moving Averages")
            df_plot = df.dropna(subset=["Close", "MA5", "MA20"])
            st.plotly_chart(line_chart_with_ma(df_plot), use_container_width=True)

            st.subheader("Top Volume Days")
            try:
                required_cols = {"Date", "Volume", "Close"}
                if required_cols.issubset(df.columns):
                    top_volume = df.sort_values(by="Volume", ascending=False).head(5)[["Date", "Volume", "Close"]]
                    top_volume["Date"] = pd.to_datetime(top_volume["Date"]).dt.strftime("%Y-%m-%d")
                    html_table = top_volume.to_html(index=False, justify="center", classes="custom-table")
                    st.markdown(f"<div class='custom-table-wrapper'>{html_table}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Top Volume Days cannot be displayed due to missing data columns.")
            except Exception as e:
                st.error(f"Failed to display top volume days: {e}")

        with tab2:
            st.subheader("Stock Chatbot Assistant")
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            for question, answer in st.session_state.chat_history:
                with st.chat_message("user"):
                    st.markdown(f"**You:** {question}")
                with st.chat_message("assistant"):
                    st.markdown(f"**Bot:** {answer}")
            user_question = st.chat_input("Ask a stock-related question...")
            if user_question:
                response = generate_stock_response(user_question, df, ticker)
                st.session_state.chat_history.append((user_question, response))
                st.rerun()

        with tab3:
            st.subheader("7-Day Forecast and Insights")
            forecast_df, forecast_plot = forecast_stock_prices(df)
            st.plotly_chart(forecast_plot, use_container_width=True)
            summary = generate_forecast_summary(ticker, forecast_df, rsi)
            st.markdown(f"**Summary:** {summary}")

        st.markdown(f"<p class='footer-time'>Last Refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>", unsafe_allow_html=True)

        with tab4:
            st.subheader(" Portfolio Tracker")

            if "portfolio" not in st.session_state:
                st.session_state.portfolio = []
            with st.expander("➕ Add a Stock to Your Portfolio"):
                with st.form("portfolio_form"):
                    st.write("Add a Stock to Your Portfolio:")
                    new_ticker = st.text_input("Stock Symbol (e.g., AAPL, TCS.NS)")
                    quantity = st.number_input("Quantity", min_value=1, step=1)
                    buy_price = st.number_input("Buy Price (₹)", min_value=0.01, step=0.5)
                    submitted = st.form_submit_button("Add")

                    if submitted and new_ticker:
                        st.session_state.portfolio.append({
                            "ticker": new_ticker.strip(),
                            "quantity": quantity,
                            "buy_price": buy_price
                        })
                        st.success(f"{new_ticker.upper()} added to your portfolio.")
                        st.rerun()
            if st.session_state.portfolio:
                df_portfolio = calculate_portfolio_metrics(st.session_state.portfolio)
                st.markdown("###  Your Portfolio Summary")
                st.dataframe(df_portfolio, use_container_width=True, height=min(400, 100 + 40 * len(df_portfolio)))
            else:
                st.info("Your portfolio is empty. Add stocks above.")

        with tab5:
            st.subheader(" Market News & Sentiment")
            try:
                articles = fetch_market_news()
                for article in articles:
                    title = article["title"]
                    description = article["description"] or ""
                    url = article["url"]
                    sentiment = analyze_sentiment(title + " " + description)

                    st.markdown(f"#### [{title}]({url})")
                    st.markdown(f"**Sentiment:** {sentiment}")
                    st.markdown(f"{description}")
                    st.markdown("---")
            except Exception as e:
                st.error(f"Failed to load news: {e}")

        with tab6:  
            st.header(" Buy / Sell / Hold Prediction")

            prediction_mode = st.radio("Choose Prediction Type:", ["Owned Stock Analysis", "Market Opportunity Analysis"])

            if prediction_mode == "Owned Stock Analysis":
                ticker_input = st.text_input("Enter Stock Ticker (e.g., TATASTEEL.NS)")
                buy_price = st.number_input("Enter Your Buy Price", min_value=0.0, step=0.1)
                if st.button("Predict for Owned Stock"):
                    if ticker_input:
                        prediction = predict_owned_stock(ticker_input, buy_price)
                        st.success(f"Recommended Action: {prediction}")
                    else:
                        st.warning("Please enter a stock ticker.")
    
            elif prediction_mode == "Market Opportunity Analysis":
                ticker_input = st.text_input("Enter Stock Ticker for Analysis (e.g., INFY.NS)")
                if st.button("Predict Market Action"):
                    if ticker_input:
                        prediction = predict_market_action(ticker_input)
                        st.success(f"Recommended Market Action: {prediction}")
                    else:
                        st.warning("Please enter a stock ticker.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
