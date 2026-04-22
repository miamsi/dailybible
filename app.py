# Version 1.2 - Streamlit Secrets (.toml) Gen Z Preacher
import streamlit as st
import random
from groq import Groq

# --- SETUP ---
st.set_page_config(page_title="The Daily Word", page_icon="⛪")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #F0F2F5; color: #1C1E21; }
    .scripture-card {
        background: linear-gradient(135deg, #ffffff 0%, #f9f9f9 100%);
        border: 2px solid #007AFF;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        color: #1C1E21;
        font-weight: bold;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .verse-label { color: #007AFF; font-size: 0.7rem; margin-top: 5px; text-transform: uppercase; letter-spacing: 1px; }
    div.stButton > button {
        background-color: #007AFF !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 10px 24px !important;
    }
    div.stButton > button:hover { background-color: #0056b3 !important; }
    .sermon-box {
        background-color: #FFFFFF;
        border-left: 5px solid #007AFF;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ---
BIBLE_BOOKS = [
    "Genesis", "Exodus", "Psalms", "Proverbs", "Isaiah", 
    "Matthew", "Mark", "Luke", "John", "Acts", 
    "Romans", "1 Corinthians", "Galatians", "Ephesians", 
    "Philippians", "Colossians", "James", "1 John", "Revelation"
]

# --- SESSION STATE ---
if 'step' not in st.session_state: st.session_state.step = "question"
if 'picks' not in st.session_state: st.session_state.picks = []
if 'user_struggle' not in st.session_state: st.session_state.user_struggle = ""

# --- CLIENT ---
try:
    # Streamlit Cloud reads the [secrets.toml] or Dashboard Secrets via this:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Missing GROQ_API_KEY in Streamlit Secrets!")
    st.stop()

# --- APP FLOW ---
st.title("⛪ The Daily Word")
st.caption("Biblically accurate, zero cap. Let's get this bread.")

if st.session_state.step == "question":
    q = st.text_input("What's the struggle today?", placeholder="My roommate is being a total NPC...")
    if st.button("Seek the Word"):
        if q:
            st.session_state.user_struggle = q
            st.session_state.picks = [] 
            st.session_state.step = "pick"
            st.rerun()

elif st.session_state.step == "pick":
    st.subheader(f"Draw 3 verses for the struggle...")
    progress = len(st.session_state.picks)
    st.write(f"Verses selected: {progress} / 3")
    
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            st.markdown('<div class="scripture-card">📜</div>', unsafe_allow_html=True)
            if st.button(f"Open Book {i+1}", key=f"pick_btn_{i}_{progress}"):
                if len(st.session_state.picks) < 3:
                    book = random.choice(BIBLE_BOOKS)
                    chapter_verse = f"{random.randint(1, 28)}:{random.randint(1, 30)}"
                    st.session_state.picks.append({"name": book, "pos": chapter_verse})
                
                if len(st.session_state.picks) == 3:
                    st.session_state.step = "reveal"
                st.rerun()

elif st.session_state.step == "reveal":
    if len(st.session_state.picks) < 3:
        st.session_state.step = "pick"
        st.rerun()
        
    st.markdown(f"### ✨ Your Daily Dose")
    p = st.session_state.picks
    
    cols = st.columns(3)
    labels = ["FOUNDATION", "STRENGTH", "PROMISE"]
    for i in range(3):
        with cols[i]:
            st.markdown(f'''
                <div class="scripture-card">
                    {p[i]["name"]}
                    <br><span class="verse-label">{p[i]["pos"]}</span>
                    <br><span style="font-size:10px; opacity:0.6;">{labels[i]}</span>
                </div>
                ''', unsafe_allow_html=True)

    with st.spinner("The Preacher is cooking..."):
        try:
            prompt = f"Struggle: {st.session_state.user_struggle}. Scripture: 1. {p[0]['name']} {p[0]['pos']}, 2. {p[1]['name']} {p[1]['pos']}, 3. {p[2]['name']} {p[2]['pos']}."
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a Biblically accurate Gen Z Preacher. Give scripture-based advice using heavy slang (no cap, slay, fr fr, glow up, rent free). Max 200 words."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192"
            )
            sermon = response.choices[0].message.content
        except:
            sermon = "Spiritual WiFi is down. Check your Secrets configuration!"

    st.markdown(f'<div class="sermon-box">{sermon}</div>', unsafe_allow_html=True)
    
    if st.button("Another Word"):
        st.session_state.step = "question"
        st.session_state.picks = []
        st.rerun()
