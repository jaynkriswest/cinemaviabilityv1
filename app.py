import streamlit as st
from formula import calculate_predictability
from api_handler import get_talent_metrics 

# 1. Initialize authentication state
if 'auth' not in st.session_state:
    st.session_state.auth = False

# 2. Authentication UI
if not st.session_state.auth:
    st.title("🎬 Producer & PR Access Portal")
    st.write("Please log in to access the Cinema Predictability Engine v3i.")
    
    email = st.text_input("Email / Agency ID")
    password = st.text_input("Password", type="password")
    
    if st.button("Access Engine"):
        # Simple local check - you can link Supabase here later
        if email: 
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Please enter your credentials.")

# 3. Main Dashboard (The ELSE that matches the IF above)
else:
    st.sidebar.title("🎥 Film Parameters")
    
    # --- PILLAR 1: TALENT (Automated via TMDB) ---
    st.sidebar.subheader("Talent Analysis")
    talent_name = st.sidebar.text_input("Lead Actor/Director Name", "Chiranjeevi")
    
    # Fetch real data using your api_handler
    total_credits, years_exp = get_talent_metrics(talent_name)
    
    # Automated Tier Logic[cite: 1]
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

    # --- PILLAR 2 & 3: MARKET & CONTENT ---[cite: 1]
    st.sidebar.subheader("Market & Script")
    market_score = st.sidebar.slider("Market Score (Screens/Reach)", 0, 100, 80)
    content_score = st.sidebar.slider("Content Quality (Script/Tech)", 0, 100, 85)
    
    # --- PILLAR 4 & 5: VIRAL & SEASONAL ---[cite: 1]
    st.sidebar.subheader("Digital & Timing")
    viral_score = st.sidebar.slider("Viral Momentum (Digital Hype)", 0, 100, 75)
    seasonal_score = st.sidebar.select_slider("Seasonal Timing", 
                                             options=[60, 75, 85, 100], 
                                             value=85,
                                             help="100 = Festival, 60 = Off-season")

    # --- GLOBAL MULTIPLIERS ---[cite: 1]
    st.sidebar.subheader("Global Modifiers")
    censor = st.sidebar.selectbox("Censor Rating", ["U (1.2x)", "UA (1.0x)", "A (0.7x)"])
    m_cert = 1.2 if "U " in censor else (0.7 if "A " in censor else 1.0)
    
    m_align = st.sidebar.slider("Marketing Alignment", 0.8, 1.0, 1.0)

    # --- ENGINE CALCULATION ---[cite: 1]
    result = calculate_predictability(
        talent_score, market_score, content_score, viral_score, seasonal_score, m_cert, m_align
    )
    
    # --- MAIN DISPLAY ---[cite: 1]
    st.title("📊 Viability Report")
    
    # Use columns for a professional look
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Predictability Score", f"{result}%")
    with col2:
        st.metric("Detected Tier", talent_tier)
    
    # Visual status bar
    st.progress(result / 100)
    
    if result >= 85:
        st.success("🔥 High Viability: Expected stable ROI with festive boost.")
    elif result >= 70:
        st.info("⚡ Moderate Viability: High reliance on Word-of-Mouth.")
    else:
        st.warning("⚠️ High Risk: Strategy pivot recommended.")

    # Strategic Action Engine[cite: 1]
    st.subheader("💡 Strategic Recommendations")
    if viral_score < 70:
        st.error("Action: Viral score is low. Release a high-energy dance track 10 days before launch.")
    if m_cert < 1.0:
        st.info("Action: 'A' Rating detected. Focus marketing on urban centers and late-night shows.")