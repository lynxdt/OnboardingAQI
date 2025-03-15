import requests
import os
from dotenv import load_dotenv
from supabase import create_client

# Load API and Supabase keys
AQI_API_KEY = os.getenv("AQI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch real-time air quality data
def fetch_air_quality(city="Kuala Lumpur"):
    url = f"https://api.waqi.info/feed/{city}/?token={AQI_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "ok":
        aqi_data = {
            "city": data["data"]["city"]["name"],
            "aqi": data["data"]["aqi"],
            "temperature": data["data"]["iaqi"].get("t", {}).get("v", None),
            "humidity": data["data"]["iaqi"].get("h", {}).get("v", None),
            "pressure": data["data"]["iaqi"].get("p", {}).get("v", None),
            "wind_speed": data["data"]["iaqi"].get("w", {}).get("v", None),
            "timestamp": data["data"]["time"]["iso"]
        }
        return aqi_data
    return None

# Store in Supabase
def store_aqi_data():
    aqi_data = fetch_air_quality()
    if aqi_data:
        response = supabase.table("air_quality").insert(aqi_data).execute()
        print("Data stored:", response)
    else:
        print("Failed to fetch data.")

# Run the function
if __name__ == "__main__":
    store_aqi_data()
