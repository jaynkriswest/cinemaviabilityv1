import requests
import os

def get_talent_metrics(name, api_key):
    # Search for the person to get their ID
    search_url = f"https://api.themoviedb.org/3/search/person?api_key={api_key}&query={name}"
    data = requests.get(search_url).json()
    
    if data['results']:
        person_id = data['results'][0]['id']
        # Fetch their full movie credits
        credits_url = f"https://api.themoviedb.org/3/person/{person_id}/movie_credits?api_key={api_key}"
        credits = requests.get(credits_url).json()
        
        count = len(credits.get('cast', []))
        # Logic: If credits > 200, they hit the Ultra-Veteran tier
        return count
    return 0