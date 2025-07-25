import streamlit as st
from auth.user_db import verify_user

def show_login():
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if verify_user(email, password):
            st.session_state.logged_in = True
            st.session_state.user = email
            st.success("Login successful!")
        else:
            st.error("Invalid email or password.")

    if st.button("Create Account"):
        st.session_state.show_signup = True
