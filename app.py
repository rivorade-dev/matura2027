import streamlit as st
import json
import os
import requests
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Matura 2027 Daily Roll", page_icon="🚀", layout="centered")

# 1. Odliczanie do matury
matura_date = datetime(2027, 5, 4, 9, 0)
now_pl = datetime.utcnow() + timedelta(hours=2) # Czas polski
days_left = (matura_date - now_pl).days

st.title("🎓 Matura 2027 Daily Roll")
st.metric(label="Dni do wielkiego finału", value=f"{days_left} dni")

# 2. Funkcja pobierania mema z Reddita
def get_reddit_meme(subreddit):
    try:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
        headers = {'User-agent': 'MaturaBot 0.1'}
        res = requests.get(url, headers=headers)
        data = res.json()
        posts = data['data']['children']
        # Filtrujemy tylko posty, które są obrazkami (nie video/tekst)
        images = [p['data']['url'] for p in posts if 'url' in p['data'] and p['data']['url'].endswith(('.jpg', '.png', '.jpeg'))]
        return random.choice(images) if images else None
    except:
        return "https://via.placeholder.com/500x300.png?text=Błąd+ładowania+mema"

# 3. Ładowanie danych z pigułkami
def get_daily_pill():
    if not os.path.exists('data.json'):
        return None, "Błąd: Brak pliku data.json!"
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            today_str = now_pl.strftime("%Y-%m-%d")
            for entry in data:
                if entry['date'] == today_str:
                    return entry, None
            return data[0], f"Szukam pigułki na {today_str}..."
    except Exception as e:
        return None, f"Błąd bazy: {e}"

pill, error_msg = get_daily_pill()

# 4. Wyświetlanie pigułek
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

# 5. SEKCJA MEMÓW
st.divider()
st.subheader("🤖 Reddit Meme of the Day")
sub = st.selectbox("Wybierz temat mema:", ["mathmemes", "physicsmemes", "ProgrammerHumor"])

if st.button("Losuj nowego mema"):
    meme_url = get_reddit_meme(sub)
    st.image(meme_url, use_column_width=True)
else:
    # Domyślny mem przy ładowaniu
    meme_url = get_reddit_meme(sub)
    st.image(meme_url, use_column_width=True)

st.caption("Aplikacja Matura 2027 | Reddit & Gemini")
