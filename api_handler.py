import requests
import streamlit as st

def get_talent_metrics(name):
    # Use Streamlit secrets for the API key to ensure it works in the cloud
    api_key = st.secrets["TMDB_API_KEY"]
    
    search_url = f"https://api.themoviedb.org/3/search/person?api_key={api_key}&query={name}"
    try:
        data = requests.get(search_url).json()
        
        if data.get('results'):
            person_id = data['results'][0]['id']
            credits_url = f"https://api.themoviedb.org/3/person/{person_id}/combined_credits?api_key={api_key}"
            credits = requests.get(credits_url).json()
            
            # 1. Total Credits (Acting + Directing)
            cast_credits = credits.get('cast', [])
            crew_credits = credits.get('crew', [])
            total_count = len(cast_credits) + len([c for c in crew_credits if c['job'] == 'Director'])
            
            # 2. Career Longevity (Difference between first release and now)
            all_releases = [c.get('release_date') for c in cast_credits if c.get('release_date')]
            if all_releases:
                first_year = int(min(all_releases)[:4])
                years_exp = 2026 - first_year
            else:
                years_exp = 0
                
            return total_count, years_exp
            
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        
    return 0, 0