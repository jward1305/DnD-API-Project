import requests
from functools import lru_cache

URL_2024 = "https://www.dnd5eapi.co/api/2024"
URL_2014 = "https://www.dnd5eapi.co/api/2014"
session24 = requests.Session()
session24.headers.update({'Accept': 'application/json'})
session14 = requests.Session()
session14.headers.update({'Accept': 'application/json'})

@lru_cache(maxsize=None)
def api_2024_request(endpoint):
    url = f"{URL_2024}/{endpoint}"
    try:
        response = session24.get(url)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during API request to {url}: {e}")
        return None
    
@lru_cache(maxsize=None)
def api_2014_request(endpoint):
    url = f"{URL_2014}/{endpoint}"
    try:
        response = session14.get(url)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during API request to {url}: {e}")
        return None

def name_to_index(name):
    return name.replace(" ", "-").lower()