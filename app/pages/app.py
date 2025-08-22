import streamlit as st
import requests
from streamlit_option_menu import option_menu
import pandas as pd

st.set_page_config(
    page_title="SmartBite",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

#Initialisierung von Session State
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# API
def get_nutrition_info(food_name):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": food_name,
        "search_simple": 1,
        "action": "process",
        "json": 1
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data["products"]:
            first = data["products"][0]
            nutriments = first.get("nutriments", {})
            return {
                "Name": first.get("product_name", "Unbekannt"),
                "Kalorien (pro 100g)": nutriments.get("energy-kcal_100g", "Keine Angabe"),
                "Fett (g)": nutriments.get("fat_100g", "Keine Angabe"),
                "Eiweiß (g)": nutriments.get("proteins_100g", "Keine Angabe"),
                "Zucker (g)": nutriments.get("sugars_100g", "Keine Angabe"),
                "Salz (g)": nutriments.get("salt_100g", "Keine Angabe")
            }
    except:
        pass
    return None

#Demo Data für History
def load_data():
    return pd.DataFrame([
        {"Gericht": "Spaghetti Carbonara", "Kalorien": 520,
         "Protein": 25, "Kohlenhydrate": 45, "Fett": 28, "Notizen": "Speck knuspriger braten!"},
        {"Gericht": "Chili sin Carne", "Kalorien": 380,
         "Protein": 18, "Kohlenhydrate": 52, "Fett": 12, "Notizen": "Perfekt scharf!"},
        {"Gericht": "Pfannkuchen", "Kalorien": 280,
         "Protein": 8, "Kohlenhydrate": 38, "Fett": 10, "Notizen": "Nächstes Mal mehr Vanille."},
    ])


# Navigationsfunktionen
def navigate_to(page_name):
    st.session_state.page = page_name



def render_navigation():
    # Navigation nur anzeigen, wenn eingeloggt
    if st.session_state.logged_in:
        selected = option_menu(
            menu_title=None,
            options=["Home", "History", "About", "Logout"],
            icons=["house", "clock-history", "info-circle", "box-arrow-right"],
            default_index=0,
            orientation="horizontal",
            key="nav_menu"
        )

        # Navigation basierend auf Auswahl aktualisieren
        if selected == "Home" and st.session_state.page != "home":
            navigate_to("home")
        elif selected == "History" and st.session_state.page != "history":
            navigate_to("history")
        elif selected == "About" and st.session_state.page != "about":
            navigate_to("about")
        elif selected == "Logout":
            st.session_state.logged_in = False
            navigate_to("login")
            st.rerun()



# ---- Seitenfunktionen ----
def show_login():
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
        resp = requests.post(
            url="http://127.0.0.1:8000/login",
            json={"username": username, "password": password}
        )
        data = resp.json()
        if data["success"]:
            st.session_state.logged_in = True
            st.success("✅ Erfolgreich eingeloggt!")
            st.session_state.page = "home"
            st.rerun()
        else:
            st.session_state.login_success = False
            st.error("❌ Falscher Benutzername oder Passwort")

    if signUp_button:
        st.info("Sign Up ist noch nicht verfügbar")

    if forgot_button:
        st.info("🔑 Funktion 'Passwort vergessen' noch nicht implementiert.")


def show_home():
    st.title("🍽️ Kalorien-Check mit OpenFoodFacts")

    food_query = st.text_input("Was hast du gegessen?")

    if st.button("Nährwerte anzeigen"):
        result = get_nutrition_info(food_query)
        if result:
            st.subheader("Nährwertangaben:")
            for key, value in result.items():
                st.write(f"**{key}**: {value}")
        else:
            st.warning("Keine passenden Daten gefunden.")


def show_history():
    st.title("🍽️ Meine Gerichte-history")

    df = load_data()

    st.subheader("📋 Meine Gerichte")
    for index, row in df.iterrows():
        with st.expander(f"🍴 {row['Gericht']} - 🔥 {row['Kalorien']} kcal"):
            st.subheader(row['Gericht'])

            # Nährwert-Karte
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Kalorien", f"{row['Kalorien']} kcal")
            with col2:
                st.metric("Protein", f"{row['Protein']}g")
            with col3:
                st.metric("Carbs", f"{row['Kohlenhydrate']}g")
            with col4:
                st.metric("Fett", f"{row['Fett']}g")


def show_about():
    st.title("Über SmartBite")
    st.write("SmartBite hilft Ihnen, Ihre Ernährung zu tracken und gesündere Entscheidungen zu treffen.")


# ---- Hauptlogik ----
def main():
    # Navigation rendern (nur wenn eingeloggt)
    render_navigation()

    # Aktuelle Seite anzeigen
    if not st.session_state.logged_in:
        show_login()
    else:
        if st.session_state.page == "home":
            show_home()
        elif st.session_state.page == "history":
            show_history()
        elif st.session_state.page == "about":
            show_about()


if __name__ == "__main__":
   main()