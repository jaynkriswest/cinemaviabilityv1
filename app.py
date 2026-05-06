import streamlit as st
from formula import calculate_predictability
from api_handler import get_talent_metrics  # Import your new logic

# ... (Keep your existing Login toggle logic here) ...

else:
    st.sidebar.title("🎥 Film Parameters")
    
    # 1. TALENT PILLAR (Automated)
    st.sidebar.subheader("Talent Analysis")
    talent_name = st.sidebar.text_input("Lead Actor/Director Name", "Chiranjeevi")
    
    # Fetch data from TMDB
    total_credits, years_exp = get_talent_metrics(talent_name)
    
    # Logic to auto-assign Talent Score based on v3i Tiers
    if total_credits >= 200 or years_exp >= 25:
        talent_tier = "Ultra-Veteran"
        talent_score = 95
    elif years_exp >= 10:
        talent_tier = "Superstar"
        talent_score = 85
    else:
        talent_tier = "Rising Star"
        talent_score = 65
    
    st.sidebar.info(f"Detected: {talent_tier} ({years_exp} yrs exp)")

    # 2. MARKET & CONTENT PILLARS
    market_score = st.sidebar.slider("Market Score (Screens/Distribution)", 0, 100, 80)
    content_score = st.sidebar.slider("Content Quality (Script/Technical)", 0, 100, 85)
    
    # 3. VIRAL & SEASONAL PILLARS
    viral_score = st.sidebar.slider("Viral Momentum (Digital Hype)", 0, 100, 75)
    seasonal_score = st.sidebar.select_slider("Seasonal Timing", 
                                             options=[60, 75, 85, 100], 
                                             value=85,
                                             help="100 = Major Festival, 60 = Off-season")

    # 4. GLOBAL MULTIPLIERS
    st.sidebar.subheader("Global Modifiers")
    censor = st.sidebar.selectbox("Censor Rating", ["U (1.2x)", "UA (1.0x)", "A (0.7x)"])
    m_cert = 1.2 if "U " in censor else (0.7 if "A " in censor else 1.0)
    
    m_align = st.sidebar.slider("Marketing Alignment (Trailer vs Film)", 0.8, 1.0, 1.0)

    # --- CALCULATION ---
    # Running all 5 pillars through the v3i formula
    result = calculate_predictability(
        talent_score, market_score, content_score, viral_score, seasonal_score, m_cert, m_align
    )
    
    # --- DISPLAY RESULTS ---
    st.header(f"Predictability Score: {result}%")
    
    if result >= 85:
        st.success("🔥 High Viability: Strong festive potential and stable ROI.")
    elif result >= 70:
        st.info("⚡ Moderate Viability: Performance depends heavily on Word-of-Mouth.")
    else:
        st.warning("⚠️ High Risk: Consider improving Viral Momentum or Marketing Alignment.")

    # Strategy Suggestions based on specific pillar weakness
    if viral_score < 70:
        st.error("Strategy: Low digital buzz detected. Recommend a high-energy 'item song' release 10 days before launch.")