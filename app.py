import streamlit as st
from streamlit_autorefresh import st_autorefresh
from components.dashboard_stock import render_stock_dashboard

st.set_page_config(page_title="Dynamic KPI Dashboard", layout="wide")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session states
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

# Auth routing
if not st.session_state.logged_in:
    if st.session_state.show_signup:
        from auth.signup import show_signup
        show_signup()
    else:
        from auth.login import show_login
        show_login()
else:
    # Sidebar + dashboard
    st.sidebar.title("📊 MetricView")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False, "user": None}))
    mode = st.sidebar.selectbox("Select Dashboard Type", ["Stock", "Sales", "Employee"])
    if mode == "Stock":
        ticker = st.sidebar.text_input("Enter Stock Symbol (e.g. AAPL, TCS.NS)", "")
        if ticker:
            render_stock_dashboard(ticker)
