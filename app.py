import streamlit as st
import json
from datetime import datetime

# 1. Konfiguracja strony (styl dark mode)
st.set_page_config(page_title="Matura 2027 Daily Roll", page_icon="🚀", layout="centered")

# 2. Odliczanie do matury
matura_date = datetime(2027, 5, 4, 9, 0)
days_left = (matura_date - datetime.now()).days

st.title("🎓 Matura 2027 Daily Roll")
st.metric(label="Dni do wielkiego finału", value=f"{days_left} dni")

# 3. Ładowanie danych (symulacja bazy JSON)
# W wersji finalnej skrypt będzie pobierał to z Twojego GitHuba
pills = [
    {
        "math": "**Optymalizacja:** Pochodna funkcji $f(x)$ w punkcie to nachylenie stycznej. Szukaj $f'(x)=0$!",
        "physics": "**Grawitacja:** Prędkość kosmiczna $v = \\sqrt{\\frac{GM}{R}}$. Nie zależy od masy satelity!",
        "polish": "**Wesele:** Chochoł to symbol uśpienia narodu. 'Miałeś chamie złoty róg...'",
        "english": "**Grammar:** *I wish I had* (żałuję, że nie mam) – konstrukcja typu 'marzenie ściętej głowy'.",
        "pdf_link": "https://cke.gov.pl/" 
    }
]

# Wyświetlanie dzisiejszej pigułki
st.divider()
st.subheader("💊 Twoja dzisiejsza dawka wiedzy:")

c1, c2 = st.columns(2)
with c1:
    with st.expander("🟦 Matematyka R", expanded=True):
        st.write(pills[0]["math"])
    with st.expander("⬜ Język Polski", expanded=True):
        st.write(pills[0]["polish"])

with c2:
    with st.expander("🟥 Fizyka R", expanded=True):
        st.write(pills[0]["physics"])
    with st.expander("🟨 Język Angielski", expanded=True):
        st.write(pills[0]["english"])

st.divider()
st.link_button("📂 Otwórz dzisiejszy arkusz CKE", pills[0]["pdf_link"])
st.caption("Aplikacja Matura 2027 | System: Gemini Engine")