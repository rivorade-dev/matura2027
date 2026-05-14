import streamlit as st
import json
import os
import requests
import urllib.request
from datetime import datetime, timedelta

st.set_page_config(page_title="Matura 2027 Daily Roll", page_icon="🚀")

# --- CZAS ---
now_pl = datetime.utcnow() + timedelta(hours=2)
st.title("🎓 Matura 2027 Daily Roll")

# --- FUNKCJA MEME (NOWA, STABILNIEJSZA) ---
def get_random_meme():
    try:
        # Używamy publicznego API do memów - nie wymaga kluczy ani cudów
        res = requests.get("https://meme-api.com/gimme/wholesomememes", timeout=5)
        return res.json()['url']
    except:
        # Backup: jeśli API padnie, dajemy klasyka
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Sad-cat.jpg/640px-Sad-cat.jpg"

# --- PIGUŁKA ---
if os.path.exists('data.json'):
    with open('data.json', 'r', encoding='utf-8') as f:
        pill = json.load(f)[0] # Bierzemy pierwszą dostępną dla testu
        st.info(f"💡 Dzisiejsza porada: {pill.get('math')}")

# --- SEKCJA MEMÓW (UPROSZCZONA DO BÓLU) ---
st.divider()
st.subheader("🔥 Losowy Mem na dziś")

# Inicjalizacja
if 'meme' not in st.session_state:
    st.session_state.meme = get_random_meme()

# Przycisk
if st.button("KLIKNIJ MNIE: Nowy mem!"):
    st.session_state.meme = get_random_meme()
    st.rerun() # Wymuszenie odświeżenia

st.image(st.session_state.meme, caption="Dostarczone przez Meme-API")
