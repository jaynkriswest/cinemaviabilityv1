def calculate_predictability(s_talent, s_market, s_content, s_viral, s_seasonal, m_cert, m_align):
    # Weights as per Cinema Predictability Model v3i
    weighted_sum = (
        (s_talent * 0.30) + 
        (s_market * 0.20) + 
        (s_content * 0.20) + 
        (s_viral * 0.15) + 
        (s_seasonal * 0.15)
    )
    # Apply global multipliers
    final_score = weighted_sum * m_cert * m_align
    return round(final_score, 2)