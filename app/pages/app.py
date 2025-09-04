import os

import streamlit as st
import requests
from streamlit_option_menu import option_menu
import pandas as pd
import openai
import io
import base64
from PIL import Image

BASE_URL = os.getenv("BACKEND_URL", "http://host.docker.internal:8000")

# Prepare OpenAI client
client = openai.OpenAI(
    api_key="ignored",
    base_url="https://models.mylab.th-luebeck.dev/v1"
)


st.set_page_config(
    page_title="SmartBite",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "access_token" not in st.session_state:
    st.session_state["access_token"] = None


def analyze_image_with_phi4(uploaded_file):
    try:
        img = Image.open(uploaded_file)

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format if img.format else 'JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        encoded_image = base64.b64encode(img_byte_arr).decode('utf-8')

        # API call to OpenAI
        chat_completion = client.chat.completions.create(
            model="phi-4-multimodal",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}" }},
                        {"type": "text", "text":
                            "Analyze the image and return only the unique name of the food or brand. "
                            "Respond only with the product or brand name, without additional words, without fantasy names. "
                            "If it's a dish, provide only the most common name (e.g., 'Currywurst'). "
                            "If it's a drink or a brand, provide exactly the brand name (e.g., 'Coca Cola', 'Sidi Ali'). "
                            "Write the name as you would find it in everyday life or in the supermarket. "
                            "Return only the name, without further explanation."
                        }
                    ]
                }
            ],
            max_tokens=1024
        )

        if chat_completion.choices and chat_completion.choices[0].message.content:
            ai_answer = chat_completion.choices[0].message.content.strip()
            st.info(f"🍴 AI recognizes: **{ai_answer}**")
            return ai_answer
        return None

    except Exception as e:
        st.error(f"Error during image analysis: {str(e)}")
        return None


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


# Navigation functions
def navigate_to(page_name):
    st.session_state.page = page_name



def render_navigation():
    # Show navigation only when logged in
    if st.session_state.logged_in:
        selected = option_menu(
            menu_title=None,
            options=["Home", "History", "About", "Logout"],
            icons=["house", "clock-history", "info-circle", "box-arrow-right"],
            default_index=0,
            orientation="horizontal",
            key="nav_menu"
        )

        # Update navigation based on selection
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


# ---- Page functions ----
def show_login():
    st.title("Welcome to SmartBite")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        col1, col2, clo3 = st.columns(3)
        with col1:
            login_button = st.form_submit_button("Login" ,use_container_width=True, type="secondary")
        with col2:
            signUp_button = st.form_submit_button("Sign Up", use_container_width=True, type="secondary")
        with clo3:
            forgot_button = st.form_submit_button("Forgot Password?", use_container_width=True, type="secondary")

    if login_button:
        try:
            resp = requests.post(
                url=f"{BASE_URL}/login",
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
                    st.success("✅ Successfully logged in!")
                    st.session_state["page"] = "home"
                    st.rerun()
                else:
                    st.error("❌ Wrong username or password")
            else:
                st.error("❌ Username doesn't exist or password is wrong")
        except requests.exceptions.RequestException:
            st.error("❌ Connection to server failed")

    if signUp_button:
        navigate_to("signUp")
        st.rerun()

    if forgot_button:
        navigate_to("forgot_password")
        st.rerun()


def show_home():
    st.title("🍽️ Calorie Check with OpenFoodFacts")

    uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is None:
        st.warning("Please take a picture.")

    if "nutrition_result" not in st.session_state:
        st.session_state.nutrition_result = None

    if st.button("Show nutritional values"):
        result = get_nutrition_info(analyze_image_with_phi4(uploaded_file))
        if result:
            st.session_state.nutrition_result = result
        else:
            st.warning("No matching data found.")
            return

    if st.session_state.nutrition_result:
        result = st.session_state.nutrition_result
        st.subheader("Nutritional information:")

        st.header(f"{result['Meal_name']}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Calories pro 100g", f"{result['Calories']} kcal")
        col1.metric("Protein", f"{result['Protein']} g")
        col2.metric("Carbs", f"{result['Carbs']} g")
        col2.metric("Fat", f"{result['Fat']} g")
        col3.metric("Sugar", f"{result['Sugar']} g")
        col3.metric("Salt", f"{result['Salt']} g")

        if st.button("Save meal", type="secondary"):
            if "access_token" not in st.session_state:
                st.warning("❌ Please log in first to save meals.")
                return
            if st.session_state["access_token"]:
                headers = {
                    "Authorization": f"Bearer {st.session_state['access_token']}",
                    "Content-Type": "application/json"
                }

                try:
                    response = requests.post(
                        url=f"{BASE_URL}/history",
                        json=result,
                        headers=headers
                    )
                    if response.status_code == 200:
                        st.success("✅ Meal saved!")
                    else:
                        st.error("❌ Error saving. Please try again.")
                except requests.exceptions.RequestException:
                    st.error("❌ Connection to server failed.")
            else:
                st.warning("Please log in first to save meals.")

def show_history():
    st.title("🍽️ My meal history")
    if "access_token" not in st.session_state:
        st.warning("❌ Please log in first to view meal history.")
        return
    if st.session_state["access_token"]:
        headers = {
            "Authorization": f"Bearer {st.session_state['access_token']}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.get(
                url=f"{BASE_URL}/history/",
                headers=headers
            )
            if response.status_code == 200:
                #st.write("Response:", response.status_code, response.json())
                data = response.json()
                if len(data) == 0:
                    st.info("No meals saved yet.")
                    return
                df = pd.DataFrame(data)
            else:
                st.error(f"Error loading history: {response.status_code}")
                return
        except requests.exceptions.RequestException:
            st.error("❌ Connection to server failed.")


    st.subheader("📋 My meals")
    for index, row in df.iterrows():
        with st.expander(f"🍴 {row['meal_name']} - 🔥 {row['calories']} kcal"):
            st.subheader(row['meal_name'])

            # Nutrition card
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

def show_about():
    st.title("About SmartBite")
    st.write("Your AI Nutrition Assistant. Snap a photo of your meal, get instant nutrition insights, and track your eating habits over time.")

def show_sign_up():
    st.title("Create new account")
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
                resp = requests.post(f"{BASE_URL}/users/", json=payload)
                if resp.status_code == 200:
                    st.success("✅ Account created! You can now log in.")
                else:
                    st.error(f"❌ Error: {resp.json()['detail']}")
            except Exception as e:
                st.error(f"❌ Connection to server failed: {e}")

    with col2:
        if st.button("Back to Login", use_container_width=True, type="secondary"):
            navigate_to("login")
            st.rerun()

def show_forgot_password():
    st.title("Reset Password")
    email_input = st.text_input("Email")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Reset Password", use_container_width=True, type="secondary"):
            payload = {
                "email": email_input
            }
            try:
                resp = requests.post(f"{BASE_URL}/users/forget_password", json=payload)
                if resp.status_code == 200:
                    st.success("✅ Please check your inbox/spam to reset your password")
                else:
                    st.error(f"❌ Error: {resp.json()['detail']}")
            except Exception as e:
                st.error(f"❌ Connection to server failed: {e}")

    with col2:
        with col2:
            if st.button("Back to Login", use_container_width=True, type="secondary"):
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