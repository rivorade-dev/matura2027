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

# 2. Bezpieczne ładowanie danych
def get_daily_pill():
    if not os.path.exists('data.json'):
        return None, "Błąd: Brak pliku data.json w repozytorium!"
    
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            today_str = datetime.now().strftime("%Y-%m-%d")
            for entry in data:
                if entry['date'] == today_str:
                    return entry, None
            return data[0], "Pokazuję pigułkę domyślną (brak wpisu na dzisiaj)."
    except json.JSONDecodeError:
        return None, "🚨 Błąd w pliku data.json! Sprawdź czy nie brakuje przecinka lub cudzysłowu."
    except Exception as e:
        return None, f"Wystąpił nieoczekiwany błąd: {e}"

pill, error_msg = get_daily_pill()

# 3. Wyświetlanie
if error_msg:
    st.warning(error_msg)

if pill:
    st.divider()
    st.subheader("💊 Twoja dzisiejsza dawka wiedzy:")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("🟦 Matematyka R", expanded=True):
            st.write(pill.get("math", "Brak danych"))
        with st.expander("⬜ Język Polski", expanded=True):
            st.write(pill.get("polish", "Brak danych"))

    with col2:
        with st.expander("🟥 Fizyka R", expanded=True):
            st.write(pill.get("physics", "Brak danych"))
        with st.expander("🟨 Język Angielski", expanded=True):
            st.write(pill.get("english", "Brak danych"))

    st.divider()
    st.link_button("📂 Otwórz arkusz", pill.get("pdf_link", "https://cke.gov.pl"))
else:
    st.info("Dodaj więcej pigułek do pliku data.json, aby zobaczyć dzisiejsze materiały!")

st.caption("Aplikacja Matura 2027 | System: Gemini Engine")
