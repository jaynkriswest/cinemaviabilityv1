import streamlit as st
from formula import calculate_predictability
from api_handler import get_talent_metrics 

# --- LOGIN BYPASS FOR TESTING ---
# We are forcing auth to True so you skip the login screen
if 'auth' not in st.session_state:
    st.session_state.auth = True 

# --- MAIN DASHBOARD ---
# This now runs automatically without asking for email/password
st.sidebar.title("Testing: Film Parameters")

# PILLAR 1: TALENT (Automated via TMDB)
st.sidebar.subheader("Talent Analysis")
talent_name = st.sidebar.text_input("Lead Actor/Director Name", "Chiranjeevi")

# Fetch real data using your api_handler
total_credits, years_exp = get_talent_metrics(talent_name)

# Automated Tier Logic
if total_credits >= 200 or years_exp >= 25:
    talent_tier = "Ultra-Veteran"
    talent_score = 95
elif years_exp >= 10:
    talent_tier = "Superstar"
    talent_score = 85
else:
    talent_tier = "Rising Star"
    talent_score = 65

st.sidebar.info(f"Tier: {talent_tier} | {years_exp} Yrs Exp")

# PILLAR 2 & 3: MARKET & CONTENT
st.sidebar.subheader("Market & Script")
market_score = st.sidebar.slider("Market Score (Screens/Reach)", 0, 100, 80)
content_score = st.sidebar.slider("Content Quality (Script/Tech)", 0, 100, 85)

# PILLAR 4 & 5: VIRAL & SEASONAL
st.sidebar.subheader("Digital & Timing")
viral_score = st.sidebar.slider("Viral Momentum (Digital Hype)", 0, 100, 75)
seasonal_score = st.sidebar.select_slider("Seasonal Timing", 
                                         options=[60, 75, 85, 100], 
                                         value=85)

# GLOBAL MULTIPLIERS[cite: 1]
st.sidebar.subheader("Global Modifiers")
censor = st.sidebar.selectbox("Censor Rating", ["U (1.2x)", "UA (1.0x)", "A (0.7x)"])
m_cert = 1.2 if "U " in censor else (0.7 if "A " in censor else 1.0)
m_align = st.sidebar.slider("Marketing Alignment", 0.8, 1.0, 1.0)

# ENGINE CALCULATION[cite: 1]
result = calculate_predictability(
    talent_score, market_score, content_score, viral_score, seasonal_score, m_cert, m_align
)

# MAIN DISPLAY[cite: 1]
st.title("Predictability Test Bench")
col1, col2 = st.columns(2)
with col1:
    st.metric("Predictability Score", f"{result}%")
with col2:
    st.metric("Detected Tier", talent_tier)

st.progress(result / 100)

if result >= 85:
    st.success("High Viability: Strong festive potential.")
elif result >= 70:
    st.info("Moderate Viability: Performance depends on WOM.")
else:
    st.warning("High Risk: Strategy pivot recommended.")