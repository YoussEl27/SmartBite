import streamlit as st
import requests

def get_nutrition_info(food_name):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": food_name,
        "search_simple": 1,
        "action": "process",
        "json": 1
    }

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
            "Salz (g)" :  nutriments.get("salt_100g", "Keine Angabe")
        }
    return None

# Streamlit UI
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
st.button("History")