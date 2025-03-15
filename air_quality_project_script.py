#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import os
from dotenv import load_dotenv
from supabase import create_client


# In[4]:


# Load API and Supabase keys from keys.env file
load_dotenv("keys.env")
API_KEY = os.getenv("AQI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# In[5]:


# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# In[6]:


# Function to fetch and clean air quality data
def get_air_quality(city_name):
    API_URL = f"https://api.waqi.info/feed/{city_name}/?token={API_KEY}"
    response = requests.get(API_URL)
    data = response.json()
    
    if data["status"] != "ok":
        return None

    aqi = data["data"]["aqi"]
    temp = data["data"]["iaqi"].get("t", {}).get("v", None)
    humidity = data["data"]["iaqi"].get("h", {}).get("v", None)

    return {
        "city": city_name,
        "aqi": aqi,
        "temperature": temp if temp is not None else "N/A",
        "humidity": humidity if humidity is not None else "N/A",
        "category": get_aqi_category(aqi)
    }


# In[9]:


# Function to categorize AQI
def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"


# In[10]:


# Function to store data in Supabase
def store_data_in_supabase(data):
    response = supabase.table("air_quality").insert([data]).execute()
    print(f"Data stored in Supabase: {response}")


# In[13]:


# Main function
def main():
    city = input("Enter city name: ")
    data = get_air_quality(city)

    if data:
        print(f"City: {data['city']}, AQI: {data['aqi']} ({data['category']})")
        store_data_in_supabase(data)
    else:
        print("Failed to fetch air quality data.")

if __name__ == "__main__":
    main()


# In[ ]:




