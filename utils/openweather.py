import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
URL_OPENWEATHER = os.getenv("URL_OPENWEATHER")
def fetch_weather_data(city_name, units="metric"):
    print(f"Fetching weather data for {API_KEY}...")
    base_url = URL_OPENWEATHER
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": units
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  
        return response.json()  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {"error": str(e)}