import streamlit as st
import plotly.graph_objs as go
import pandas as pd
from utils.kpi_calculator import calculate_employee_kpis
from datetime import datetime
from config.style_config import GAUGE_THRESHOLDS
from utils.layout_utils import create_gauge, bar_chart

def render_employee_dashboard(df: pd.DataFrame):
    st.header("🧑‍💼 Employee Performance Dashboard")

    # Calculate KPIs
    kpis = calculate_employee_kpis(df)

    # === Top Metrics ===
    st.subheader("📊 Summary KPIs")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tasks Done", f"{kpis['Total Tasks Done']}")
    col2.metric("Bugs Resolved", f"{kpis['Bugs Resolved']}")
    col3.metric("Avg Productivity", f"{kpis['Avg Productivity (%)']}%")
    col4.metric("Avg Attendance", f"{kpis['Avg Attendance (%)']}%")

    # === Gauges ===
    st.subheader("📌 Performance Gauges")
    gauge_col1, gauge_col2 = st.columns(2)
    with gauge_col1:
        st.plotly_chart(create_gauge("Productivity %", kpis['Avg Productivity (%)'], 0, 100), use_container_width=True)
    with gauge_col2:
        st.plotly_chart(create_gauge("Attendance %", kpis['Avg Attendance (%)'], 0, 100), use_container_width=True)

    # === Productivity by Employee (Bar Chart) ===
    st.subheader("📈 Employee-wise Productivity")
    if "Name" in df.columns and "Productivity" in df.columns:
        chart = bar_chart(df, "Name", "Productivity")
        st.plotly_chart(chart, use_container_width=True)
    else:
        st.warning("Required columns ('Name', 'Productivity') not found.")

    # === Leaderboard Table (Top Performers) ===
    st.subheader("🏆 Top Performers")
    if "Name" in df.columns and "TasksDone" in df.columns:
        top = df[["Name", "TasksDone"]].groupby("Name").sum().sort_values(by="TasksDone", ascending=False).head(5)
        st.table(top.rename(columns={"TasksDone": "Total Tasks"}))
    else:
        st.warning("Leaderboard data missing.")

    # === Footer Clock ===
    st.markdown(f"<p class='footer-time'>Last Refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>", unsafe_allow_html=True)


# === Helpers ===

def create_gauge(title, value, min_val, max_val):
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={'axis': {'range': [min_val, max_val]}},
    ))

def bar_chart(df, name_col, value_col):
    df = df.groupby(name_col)[value_col].mean().reset_index()
    fig = go.Figure(data=[
        go.Bar(x=df[name_col], y=df[value_col], marker_color='teal')
    ])
    fig.update_layout(xaxis_title=name_col, yaxis_title=value_col, height=400, margin=dict(l=0, r=0, t=20, b=0))
    return fig
