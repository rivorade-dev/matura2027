import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Matura 2027 Daily Roll", page_icon="🚀", layout="centered")

# 1. Odliczanie
matura_date = datetime(2027, 5, 4, 9, 0)
days_left = (matura_date - datetime.now()).days

st.title("🎓 Matura 2027 Daily Roll")
st.metric(label="Dni do wielkiego finału", value=f"{days_left} dni")

# 2. Funkcja do ładowania pigułki na dziś
def get_daily_pill():
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            today_str = datetime.now().strftime("%Y-%m-%d")
            for entry in data:
                if entry['date'] == today_str:
                    return entry
            return data[0] # Jeśli nie ma na dziś, pokaż pierwszą
    return None

pill = get_daily_pill()

# 3. Wyświetlanie
if pill:
    st.divider()
    st.subheader("💊 Twoja dzisiejsza dawka wiedzy:")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("🟦 Matematyka R", expanded=True):
            st.write(pill["math"])
        with st.expander("⬜ Język Polski", expanded=True):
            st.write(pill["polish"])

    with col2:
        with st.expander("🟥 Fizyka R", expanded=True):
            st.write(pill["physics"])
        with st.expander("🟨 Język Angielski", expanded=True):
            st.write(pill["english"])

    st.divider()
    st.link_button("📂 Otwórz dzisiejszy arkusz CKE", pill["pdf_link"])
else:
    st.error("Nie znaleziono pliku data.json lub dzisiejszej pigułki!")

st.caption("Aplikacja Matura 2027 | Streamlit & Gemini")
