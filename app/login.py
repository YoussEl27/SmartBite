import streamlit as st

st.title("Willkommen bei SmartBite")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2, clo3 = st.columns(3)
    with col1:
        login_button = st.form_submit_button("Login")
    with col2:
        signUp_button = st.form_submit_button("Sign Up")
    with clo3:
        forgot_button = st.form_submit_button("Passwort vergessen")


if login_button:
    if username == "admin" and password == "1234":  # <-- wird später mit DB angepasst
        st.session_state.logged_in = True
        st.success("✅ Erfolgreich eingeloggt!")

    else:
           st.session_state.logged_in = False
           st.error("❌ Falscher Benutzername oder Passwort")

if forgot_button:
    st.info("🔑 Funktion 'Passwort vergessen' noch nicht implementiert.")

if signUp_button:
    st.info("Sign Up ist noch nicht verfügbar")

