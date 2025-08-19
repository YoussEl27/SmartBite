import streamlit as st

st.title("SmartBite")
st.text("Sign up to see how many you eat HAHAHA")

first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
password = st.text_input("Password", type="password")
age = st.number_input("Age", min_value=0, max_value=120)
email = st.text_input("Email")
phone_number = st.text_input("Phone Number")

if st.button("Sign Up"):
    st.success("Registration completed!")