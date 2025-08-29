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
if "access_token" not in st.session_state:
    st.session_state["access_token"] = None


# API
def get_nutrition_info(food_name):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": food_name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 3
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data["products"]:
            first = data["products"][0]
            nutriments = first.get("nutriments", {})
            return {
                "Meal_name"    : first.get("product_name", "Unknown"),
                "Calories": nutriments.get("energy-kcal_100g", "Not specified"),
                "Protein": nutriments.get("proteins_100g", "Not specified"),
                "Carbs": nutriments.get("carbohydrates_100g", "Not specified"),
                "Fat"     : nutriments.get("fat_100g", "Not specified"),
                "Sugar"   : nutriments.get("sugars_100g", "Not specified"),
                "Salt"    : nutriments.get("salt_100g", "Not specified"),
            }
    except:
        pass
    return None


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
            forgot_button = st.form_submit_button("Passwort vergessen?")

    if login_button:
        try:
            resp = requests.post(
                url="http://127.0.0.1:8000/login",
                json={"username": username, "password": password},
                timeout=5
            )
            #st.write("Login Response:", resp.status_code, resp.json())
            if resp.status_code == 200:
                data = resp.json()
                token = data.get("access_token")
                if token:
                    st.session_state["access_token"] = token
                    st.session_state["logged_in"] = True
                    st.success("✅ Erfolgreich eingeloggt!")
                    st.session_state["page"] = "home"
                    st.rerun()
                else:
                    st.error("❌ Falscher Benutzername oder Passwort")
            else:
                st.error("❌ Username existiert nicht oder Passwort falsch")
        except requests.exceptions.RequestException:
            st.error("❌ Verbindung zum Server fehlgeschlagen")

    if signUp_button:
        navigate_to("signUp")
        st.rerun()

    if forgot_button:
        navigate_to("passwort_vergessen")
        st.rerun()


def show_home():
    st.title("🍽️ Kalorien-Check mit OpenFoodFacts")

    food_query = st.text_input("Was hast du gegessen?")

    if "nutrition_result" not in st.session_state:
        st.session_state.nutrition_result = None

    if st.button("Nährwerte anzeigen"):
        result = get_nutrition_info(food_query)
        if result:
            st.session_state.nutrition_result = result
        else:
            st.warning("Keine passenden Daten gefunden.")

    if st.session_state.nutrition_result:
        result = st.session_state.nutrition_result
        st.subheader("Nährwertangaben:")

        st.header(f"{result['Meal_name']}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Calories", f"{result['Calories']} kcal")
        col1.metric("Protein", f"{result['Protein']} g")
        col2.metric("Carbs", f"{result['Carbs']} g")
        col2.metric("Fett", f"{result['Fat']} g")
        col3.metric("Sugar", f"{result['Sugar']} g")
        col3.metric("Salt", f"{result['Salt']} g")

        if st.button("Meal speichern", type="secondary"):
            if "access_token" not in st.session_state:
                st.warning("❌ Bitte zuerst einloggen, um Mahlzeiten zu speichern.")
                return
            if st.session_state["access_token"]:
                headers = {
                    "Authorization": f"Bearer {st.session_state['access_token']}",
                    "Content-Type": "application/json"
                }

                try:
                    response = requests.post(
                        url="http://127.0.0.1:8000/history",
                        json=result,
                        headers=headers
                    )
                    if response.status_code == 200:
                        st.success("✅ Mahlzeit wurde gespeichert!")
                    else:
                        st.error("❌ Fehler beim Speichern. Bitte erneut versuchen.")
                except requests.exceptions.RequestException:
                    st.error("❌ Verbindung zum Server fehlgeschlagen.")
            else:
                st.warning("Bitte zuerst einloggen, um Mahlzeiten zu speichern.")

def show_history():
    st.title("🍽️ Meine Gerichte-history")
    if "access_token" not in st.session_state:
        st.warning("❌ Bitte zuerst einloggen, um Mahlzeiten zu speichern.")
        return
    if st.session_state["access_token"]:
        headers = {
            "Authorization": f"Bearer {st.session_state['access_token']}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.get(
                url="http://127.0.0.1:8000/history/",
                headers=headers
            )
            if response.status_code == 200:
                #st.write("Response:", response.status_code, response.json())
                data = response.json()
                if len(data) == 0:
                    st.info("Noch keine Gerichte gespeichert.")
                    return
                df = pd.DataFrame(data)
            else:
                st.error(f"Fehler beim Laden der History: {response.status_code}")
                return
        except requests.exceptions.RequestException:
            st.error("❌ Verbindung zum Server fehlgeschlagen.")


    st.subheader("📋 Meine Gerichte")
    for index, row in df.iterrows():
        with st.expander(f"🍴 {row['meal_name']} - 🔥 {row['calories']} kcal"):
            st.subheader(row['meal_name'])

            # Nährwert-Karte
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Calories", f"{row['calories']} kcal")
            with col2:
                st.metric("Protein", f"{row['protein']}g")
            with col3:
                st.metric("Carbs", f"{row['carbs']}g")
            with col4:
                st.metric("Fat", f"{row['fat']}g")
            with col5:
                st.metric("Sugar", f"{row['sugar']}g")
            #with col6:
             #   st.metric("Salt", f"{row['salt']}g")

def show_about():
    st.title("Über SmartBite")
    st.write("SmartBite hilft Ihnen, Ihre Ernährung zu tracken und gesündere Entscheidungen zu treffen.")

def show_sign_up():
    st.title("Neuen Account erstellen")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sign Up",use_container_width=True, type="secondary"):
            payload = {
                "username": username,
                "password": password,
                "email": email
            }
            try:
                resp = requests.post("http://127.0.0.1:8000/users/", json=payload)
                if resp.status_code == 200:
                    st.success("✅ Account erstellt! Du kannst dich jetzt einloggen.")
                else:
                    st.error(f"❌ Fehler: {resp.json()['detail']}")
            except Exception as e:
                st.error(f"❌ Verbindung zum Server fehlgeschlagen: {e}")

    with col2:
        if st.button("Zurück zum Login", use_container_width=True, type="secondary"):
            navigate_to("login")
            st.rerun()

def show_forgot_password():
    st.title("Passwort zurücksetzen")
    email_input = st.text_input("Email")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Passwort zurücksetzen", use_container_width=True, type="secondary"):
            payload = {
                "email": email_input
            }
            try:
                resp = requests.post("http://127.0.0.1:8000/users/forget_password", json=payload)
                if resp.status_code == 200:
                    st.success("✅ Checken Sie bitte Ihre Postfach/Spam ein, um Ihre Passwort zurücksetzen")
                else:
                    st.error(f"❌ Fehler: {resp.json()['detail']}")
            except Exception as e:
                st.error(f"❌ Verbindung zum Server fehlgeschlagen: {e}")

    with col2:
        with col2:
            if st.button("Zurück zum Login", use_container_width=True, type="secondary"):
                navigate_to("login")
                st.rerun()


def main():
    render_navigation()


    if not st.session_state.logged_in:
        if st.session_state.page == "login":
            show_login()
        elif st.session_state.page == "signUp":
            show_sign_up()
        else:
            show_forgot_password()
    else:
        if st.session_state.page == "home":
            show_home()
        elif st.session_state.page == "history":
            show_history()
        elif st.session_state.page == "about":
            show_about()

if __name__ == "__main__":
   main()