from utils.openweather import fetch_weather_data

def get_weather_for_homepage(city_name="Ho Chi Minh"):

    weather_data = fetch_weather_data(city_name)
    if "error" in weather_data:
        return {"error": weather_data["error"]}
    
    extracted_data = {
        "city": weather_data.get("name", "Unknown"),
        "temperature": weather_data.get("main", {}).get("temp", "N/A"),
        "humidity": weather_data.get("main", {}).get("humidity", "N/A"),
        "pressure": weather_data.get("main", {}).get("pressure", "N/A"),
        "description": weather_data.get("weather", [{}])[0].get("description", "N/A"),
        "wind_speed": weather_data.get("wind", {}).get("speed", "N/A"),
    }
    return extracted_data