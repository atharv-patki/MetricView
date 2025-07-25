import streamlit as st
from auth.user_db import create_user
from utils.email_sender import send_welcome_email  # ✅ Import email sender

def show_signup():
    st.title("Create Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match.")
        else:
            success = create_user(email, password)
            if success:
                # ✅ Send welcome email
                if send_welcome_email(email):
                    st.success("Account created and welcome email sent!")
                else:
                    st.warning("Account created, but failed to send welcome email.")
                st.session_state.show_signup = False
            else:
                st.error("User already exists.")

    if st.button("Back to Login"):
        st.session_state.show_signup = False
