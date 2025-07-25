# secure_view_feedback.py
import streamlit as st
import pandas as pd
import os
import bcrypt

# --- Secure Admin Credentials (bcrypt hashes) ---
admin_credentials = {
    "admin1": b"pass",  #create pass
    "admin2": b"pass"   #create pass
}

# --- Session Init ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "admin_user" not in st.session_state:
    st.session_state.admin_user = ""

# --- Login Page ---
if not st.session_state.logged_in:
    st.title(" Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in admin_credentials and bcrypt.checkpw(password.encode(), admin_credentials[username]):
            st.success("✅ Login successful")
            st.session_state.logged_in = True
            st.session_state.admin_user = username
            st.rerun()
        else:
            st.error("❌ Invalid username or password")
    st.stop()

# --- Sidebar: Logout ---
with st.sidebar:
    st.markdown(f"👤 Logged in as: `{st.session_state.admin_user}`")
    if st.button(" Logout"):
        st.session_state.logged_in = False
        st.session_state.admin_user = ""
        st.rerun()

# --- View Feedbacks ---
st.title("📬 Feedback Submissions")
feedback_file = "data/feedback.csv"

if os.path.exists(feedback_file):
    df = pd.read_csv(feedback_file)
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No feedback submitted yet.")
else:
    st.info("No feedback submitted yet.")