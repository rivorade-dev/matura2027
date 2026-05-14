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
        # Nagłówki udające prawdziwą przeglądarkę
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=50"
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status() # Sprawdź czy nie ma błędu HTTP
        
        data = res.json()
        posts = data['data']['children']
        
        # Szukamy tylko obrazków
        images = [p['data']['url'] for p in posts if 'url' in p['data'] and any(p['data']['url'].endswith(ext) for ext in ['.jpg', '.png', '.jpeg'])]
        
        if images:
            return random.choice(images)
        return "https://via.placeholder.com/500x300.png?text=Brak+obrazkow+na+liście"
    except Exception as e:
        return f"https://via.placeholder.com/500x300.png?text=Reddit+Error:+{str(e)[:20]}"

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

# --- SEKCJA MEMÓW (UPROSZCZONA) ---
st.divider()
st.subheader("🤖 Reddit Meme of the Day")

sub = st.selectbox("Wybierz temat:", ["mathmemes", "physicsmemes", "ProgrammerHumor"])

# Używamy st.button w prosty sposób
if st.button("🔄 Losuj nowego mema"):
    new_meme = get_reddit_meme(sub)
    st.session_state['meme_url'] = new_meme

# Inicjalizacja obrazka przy pierwszym wejściu
if 'meme_url' not in st.session_state:
    st.session_state['meme_url'] = get_reddit_meme(sub)

st.image(st.session_state['meme_url'], use_container_width=True)

st.caption("Aplikacja Matura 2027 | Reddit & Gemini")
