import streamlit as st
import re

st.title("🔐 Forgot your password?")

email = st.text_input("Enter your email address")

if st.button("Send Reset Link", type="primary"):
    if not email:
        st.error("Please enter your email address")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.error("Please enter a valid email address")
    else:
        st.success("✅ We have sent a password reset link to your email!")
        st.info("Check your inbox and also the spam folder")