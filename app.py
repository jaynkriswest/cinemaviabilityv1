import streamlit as st
from datetime import date
from formula import calculate_predictability
from api_handler import get_talent_metrics 

# --- CONFIGURATION & UI THEME ---
st.set_page_config(page_title="Cinema Predictability Engine v3i", layout="wide")

# --- LOGIN BYPASS FOR TESTING ---
if 'auth' not in st.session_state:
    st.session_state.auth = True 

# --- MAIN INTERFACE ---
st.title("🎬 Cinema Viability & ROI Predictor")
st.markdown("---")

# Use Columns to separate inputs from the results dashboard
col_input, col_display = st.columns([1, 2], gap="large")

with col_input:
    st.header("Project Blueprint")
    
    # 1. TALENT PILLAR (Searchable)
    talent_name = st.text_input("Lead Talent (Actor/Director)", value="Chiranjeevi", help="Linked to TMDB Real-time Data")
    total_credits, years_exp = get_talent_metrics(talent_name)
    
    # Logic to auto-assign Talent Score based on v3i Tiers
    if total_credits >= 200 or years_exp >= 25:
        talent_tier, talent_score = "Ultra-Veteran", 95
    elif years_exp >= 10:
        talent_tier, talent_score = "Superstar", 85
    else:
        talent_tier, talent_score = "Rising Star", 65
    
    st.info(f"Analysis: {talent_tier} | {years_exp} Years Experience")

    # 2. FINANCIALS & SCALE (Replacing Market Sliders)
    st.subheader("Financial Scale")
    budget = st.number_input("Production Budget (in Crores)", min_value=1, value=50)
    market_reach = st.selectbox("Distribution Strategy", 
                                ["Limited (Single State)", "Standard (South India)", "Pan-India", "Global Release"])
    
    # Internal mapping for Market Score
    market_map = {"Limited (Single State)": 65, "Standard (South India)": 80, "Pan-India": 90, "Global Release": 100}
    market_score = market_map[market_reach]

    # 3. CONTENT & REMAKE LOGIC (Addressing the Remake Paradox)
    st.subheader("Script & Execution")
    genre = st.selectbox("Primary Genre", ["Mass Action", "Social Drama", "Thriller", "Romance", "Remake/Adaptation"])
    
    script_strength = st.selectbox("Script/Source Material Confidence", 
                                   ["Original - High Risk", "Original - High Potential", "Proven Source (Remake/Novel)"])
    # Logic: Remakes start with higher base reliability but lower viral 'freshness'
    content_score = 90 if script_strength == "Proven Source (Remake/Novel)" else 75

    # 4. SCHEDULING (Calendar Picker)
    st.subheader("Release Scheduling")
    release_date = st.date_input("Target Release Date", value=None, help="Select a date to calculate Seasonal Timing")
    
    if release_date:
        # Simple logic: Festivals like Sankranti (Jan) or Diwali (Oct/Nov) boost scores[cite: 1]
        month = release_date.month
        if month in [1, 4, 10, 12]: # Festive/Holiday months
            seasonal_score = 100
        else:
            seasonal_score = 75
    else:
        seasonal_score = 75 # Neutral score if no date is picked

    # 5. MULTIPLIERS
    st.subheader("Global Multipliers")
    censor = st.radio("Target Censor Rating", ["U", "UA", "A"], horizontal=True)
    m_cert = 1.2 if censor == "U" else (0.7 if censor == "A" else 1.0)
    
    m_align = st.select_slider("Marketing & Promo Alignment", options=[0.8, 0.85, 0.9, 0.95, 1.0], value=1.0)

with col_display:
    st.header("Viability Analysis")
    
    # CALCULATE
    raw_result = calculate_predictability(talent_score, market_score, content_score, 80, seasonal_score, m_cert, m_align)
    result = min(raw_result, 98.0) # Realism Cap[cite: 1]
    
    # METRICS DISPLAY
    m1, m2, m3 = st.columns(3)
    m1.metric("Predictability", f"{result}%")
    m2.metric("Market Tier", market_reach)
    m3.metric("Project Type", genre)
    
    st.progress(result / 100)
    
    # DYNAMIC STRATEGY GENERATOR
    st.markdown("### Executive Strategy")
    if genre == "Remake/Adaptation" and talent_tier != "Ultra-Veteran":
        st.warning("**Risk Alert:** Remakes with non-veteran leads require 20% higher marketing spend to overcome 'Comparison Fatigue'.")
    
    if budget > 100 and market_reach != "Pan-India":
        st.error("**Financial Mismatch:** Heavyweight budgets (>100Cr) are highly unpredictable without Pan-India distribution reach.")
    
    if result >= 90:
        st.success("**Greenlight Recommended:** Strong stability metrics across all pillars.")
    else:
        st.info("**Optimization Required:** Consider shifting release to a festive window to improve Seasonal Score.")