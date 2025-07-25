import streamlit as st
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime

from utils.kpi_calculator import calculate_sales_kpis
from utils.layout_utils import create_gauge, bar_chart
from utils.report_generator import generate_kpi_report
from config.kpi_config import SALES_KPIS
from config.style_config import GAUGE_THRESHOLDS



def render_sales_dashboard(df):
    st.header("💰 Sales KPI Dashboard")

    # === Calculate KPIs ===
    kpis = calculate_sales_kpis(df)

    # === Top Metrics ===
    st.subheader("📊 Key Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"₹{kpis['Total Revenue']}")
    col2.metric("Avg Order Value", f"₹{kpis['Avg Order Value']}")
    col3.metric("Conversion Rate", f"{kpis['Conversion Rate (%)']}%")
    col4.metric("Avg Lead Time", f"{kpis['Avg Lead Time (Days)']} days")

    # === Gauges ===
    st.subheader("📌 Performance Gauges")
    gauge_col1, gauge_col2 = st.columns(2)
    with gauge_col1:
        st.plotly_chart(
            create_gauge(
                "Conversion Rate (%)",
                kpis['Conversion Rate (%)'],
                0,
                100
            ),
            use_container_width=True
        )
    with gauge_col2:
        st.plotly_chart(
            create_gauge(
                "Avg Order Value",
                kpis['Avg Order Value'],
                0,
                max(df["OrderValue"].max(), 1)
            ),
            use_container_width=True
        )

    # === Revenue Line Chart ===
    st.subheader("📈 Revenue Trend")
    if "Date" in df.columns and "Revenue" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        st.plotly_chart(revenue_line_chart(df), use_container_width=True)
    else:
        st.warning("Date or Revenue column missing for trend analysis.")

    # === Leaderboard ===
    st.subheader("🏆 Sales Leaderboard (by Rep)")
    leaderboard_col = "Rep" if "Rep" in df.columns else df.columns[0]
    table = df.groupby(leaderboard_col)["Revenue"].sum().sort_values(ascending=False).reset_index().head(5)
    table.columns = ["Name", "Total Revenue"]
    st.table(table.set_index("Name"))

    # === Footer Clock ===
    st.markdown(f"<p class='footer-time'>Last Refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>", unsafe_allow_html=True)

    # === Report Generation ===
    kpi_data = kpis
    leaderboard = table.to_dict(orient="records")

    report_path = generate_kpi_report(
        title="Sales KPI Report",
        kpi_sections=[
            {"title": "KPI Summary", "data": [{"Metric": k, "Value": v} for k, v in kpi_data.items()]},
            {"title": "Top Performers", "data": leaderboard}
        ]
    )

    st.success(f"✅ Report generated!")
    st.download_button("Download KPI Report (PDF)", data=open(report_path, "rb").read(), file_name="sales_report.pdf")


# === Helpers ===

def revenue_line_chart(df):
    trend = df.groupby("Date")["Revenue"].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=trend["Date"], y=trend["Revenue"], mode='lines+markers', name='Revenue'))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=400)
    return fig
