import streamlit as st
import json
import os
import requests
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Matura 2027 Daily Roll", page_icon="🚀", layout="centered")

# --- LOGIKA CZASU ---
matura_date = datetime(2027, 5, 4, 9, 0)
now_pl = datetime.utcnow() + timedelta(hours=2)
days_left = (matura_date - now_pl).days

st.title("🎓 Matura 2027 Daily Roll")
st.metric(label="Dni do wielkiego finału", value=f"{days_left} dni")

# --- FUNKCJA REDDIT ---
def get_reddit_meme(subreddit):
    try:
        # Dodajemy losowy parametr, żeby oszukać cache Reddita
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=30"
        headers = {'User-agent': 'MaturaBot 0.2'}
        res = requests.get(url, headers=headers)
        data = res.json()
        posts = data['data']['children']
        # Filtrujemy obrazki
        images = [p['data']['url'] for p in posts if 'url' in p['data'] and p['data']['url'].endswith(('.jpg', '.png', '.jpeg'))]
        return random.choice(images) if images else "https://via.placeholder.com/500x300.png?text=Brak+obrazkow+na+Reddit"
    except Exception as e:
        return f"https://via.placeholder.com/500x300.png?text=Blad+polaczenia+z+Reddit"

# --- ŁADOWANIE PIGUŁKI ---
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
            return data[0]
    except:
        return None

pill = get_daily_pill()

# --- WYŚWIETLANIE PIGUŁEK ---
if pill:
    st.divider()
    st.subheader("💊 Twoja dzisiejsza dawka wiedzy:")
    c1, c2 = st.columns(2)
    with c1:
        with st.expander("🟦 Matematyka R", expanded=True):
            st.write(pill.get("math"))
        with st.expander("⬜ Język Polski", expanded=True):
            st.write(pill.get("polish"))
    with c2:
        with st.expander("🟥 Fizyka R", expanded=True):
            st.write(pill.get("physics"))
        with st.expander("🟨 Język Angielski", expanded=True):
            st.write(pill.get("english"))
    
    st.link_button("📂 Otwórz Arkusze.pl", "https://arkusze.pl/")

# --- SEKCJA MEMÓW (NAPRAWIONA) ---
st.divider()
st.subheader("🤖 Reddit Meme of the Day")

sub = st.selectbox("Wybierz temat mema:", ["mathmemes", "physicsmemes", "ProgrammerHumor"])

# Inicjalizacja mema w pamięci sesji, jeśli go nie ma
if 'current_meme' not in st.session_state:
    st.session_state.current_meme = get_reddit_meme(sub)

# Przycisk do losowania
if st.button("🔄 Losuj nowego mema"):
    st.session_state.current_meme = get_reddit_meme(sub)

# Wyświetlanie mema z pamięci sesji
st.image(st.session_state.current_meme, use_container_width=True)

st.caption("Aplikacja Matura 2027 | Reddit & Gemini")
