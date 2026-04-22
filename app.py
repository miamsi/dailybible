# Version 1.4 - Fixed Syntax & Direct Revelation
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
        background: white;
        border: 2px solid #007AFF;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    .verse-label { color: #007AFF; font-size: 0.7rem; font-weight: bold; text-transform: uppercase; }
    .sermon-box {
        background-color: #FFFFFF;
        border-left: 5px solid #007AFF;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        font-size: 1.1rem;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True) # Fixed parameter name here

# --- DATA ---
BIBLE_BOOKS = [
    "Genesis", "Exodus", "Psalms", "Proverbs", "Isaiah", 
    "Matthew", "Mark", "Luke", "John", "Acts", 
    "Romans", "1 Corinthians", "Galatians", "Ephesians", 
    "Philippians", "Colossians", "James", "1 John", "Revelation"
]

# --- CLIENT ---
try:
    # Ensure GROQ_API_KEY is in your Streamlit Cloud Secrets
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("⚠️ Secrets Error: Check your Streamlit Cloud Secrets dashboard for GROQ_API_KEY.")
    st.stop()

# --- APP UI ---
st.title("⛪ The Daily Word")
st.caption("Biblically accurate, zero cap. Facing your struggles with main character energy.")

# Input Section
struggle = st.text_input("What's heavy on your spirit today?", placeholder="Lowkey feeling burnt out...")

if st.button("Get the Word"):
    if struggle:
        # Generate 3 random verses immediately
        verses = []
        for _ in range(3):
            book = random.choice(BIBLE_BOOKS)
            ref = f"{random.randint(1, 28)}:{random.randint(1, 30)}"
            verses.append({"book": book, "ref": ref})

        # Display the Verses
        st.markdown("### ✨ Your Revelation")
        cols = st.columns(3)
        labels = ["FOUNDATION", "STRENGTH", "PROMISE"]
        for i, col in enumerate(cols):
            with col:
                st.markdown(f'''
                    <div class="scripture-card">
                        <span class="verse-label">{labels[i]}</span><br>
                        <strong>{verses[i]['book']}</strong><br>
                        {verses[i]['ref']}
                    </div>
                    ''', unsafe_allow_html=True)

        # Generate AI Sermon
        with st.spinner("The Preacher is typing..."):
            try:
                prompt = f"""
                Struggle: {struggle}
                Verses assigned: 
                1. {verses[0]['book']} {verses[0]['ref']}
                2. {verses[1]['book']} {verses[1]['ref']}
                3. {verses[2]['book']} {verses[2]['ref']}
                """
                
                # Using a standard stable model ID
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a Biblically accurate Gen Z Preacher. Give actual scripture-based wisdom using Gen Z slang (no cap, slay, fr fr, glow up, rent free). Max 180 words."},
                        {"role": "user", "content": prompt}
                    ],
                    model="meta-llama/llama-4-scout-17b-16e-instruct" 
                )
                sermon = response.choices[0].message.content
                st.markdown(f'<div class="sermon-box">{sermon}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"WiFi Lag: {str(e)}")
    else:
        st.warning("Tell me what's up so I can pray for the vibes.")
