import streamlit as st
import json
import os
import requests
from datetime import datetime, timedelta

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Matura 2027 Daily Roll", page_icon="🎓", layout="centered")

# --- LOGIKA CZASU (POLSKA) ---
# Serwery Streamlit są w UTC, dodajemy 2h dla czasu polskiego letniego
now_pl = datetime.utcnow() + timedelta(hours=2)
matura_date = datetime(2027, 5, 4, 9, 0)
days_left = (matura_date - now_pl).days

st.title("🎓 Matura 2027 Daily Roll")
st.metric(label="Dni do wielkiego finału", value=f"{days_left} dni")

# --- FUNKCJE POMOCNICZE ---
def get_daily_pill():
    if not os.path.exists('data.json'):
        return None
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            today_str = now_pl.strftime("%Y-%m-%d")
            for entry in data:
                if entry['date'] == today_str:
                    return entry
            return data[0] # Fallback do pierwszej pigułki
    except:
        return None

def get_random_meme():
    try:
        # Możesz zmienić 'wholesomememes' na 'mathmemes' lub 'physicsmemes'
        res = requests.get("https://meme-api.com/gimme/physicsmemes", timeout=5)
        return res.json()['url']
    except:
        return "https://via.placeholder.com/500x300.png?text=Problemy+z+siecią+u+Reddita"

# --- WYŚWIETLANIE PIGUŁEK ---
pill = get_daily_pill()

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
    st.link_button("📂 Otwórz Arkusze.pl (Wybierz przedmiot)", "https://arkusze.pl/")
else:
    st.error("Błąd ładowania pigułek! Sprawdź plik data.json.")

# --- SEKCJA MEMÓW ---
st.divider()
st.subheader("🔥 Losowy Mem dla Mat-Fizu")

if 'meme_url' not in st.session_state:
    st.session_state.meme_url = get_random_meme()

if st.button("🔄 Losuj nowego mema"):
    st.session_state.meme_url = get_random_meme()
    st.rerun()

st.image(st.session_state.meme_url, use_container_width=True)

st.caption(f"Aktualizacja systemu: {now_pl.strftime('%Y-%m-%d %H:%M')}")
