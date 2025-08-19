import streamlit as st
import pandas as pd


# Beispiel Nährwerten
def load_data():
    return pd.DataFrame([
        {"Gericht": "Spaghetti Carbonara", "Kalorien": 520,
         "Protein": 25, "Kohlenhydrate": 45, "Fett": 28, "Notizen": "Speck knuspriger braten!"},
        {"Gericht": "Chili sin Carne", "Kalorien": 380,
         "Protein": 18, "Kohlenhydrate": 52, "Fett": 12, "Notizen": "Perfekt scharf!"},
        {"Gericht": "Pfannkuchen", "Kalorien": 280,
         "Protein": 8, "Kohlenhydrate": 38, "Fett": 10, "Notizen": "Nächstes Mal mehr Vanille."},
    ])


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


