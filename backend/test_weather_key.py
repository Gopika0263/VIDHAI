from dotenv import load_dotenv
import os
import requests

# Load .env variables
load_dotenv()
API_KEY = os.getenv("OWM_API_KEY")

# Show the key with quotes to check for spaces
print(f"Loaded API Key: '{API_KEY}'")

if not API_KEY:
    print("⚠️ No API key found in .env. Please add OWM_API_KEY=your_key")
    exit(1)

# Test OpenWeatherMap API
url = "https://api.openweathermap.org/data/2.5/weather"
params = {"q": "Chennai", "appid": API_KEY, "units": "metric"}

try:
    response = requests.get(url, params=params)
    data = response.json()
    
    if response.status_code == 200:
        temp = data['main']['temp']
        condition = data['weather'][0]['description']
        print(f"🌤 Weather in Chennai: {temp}°C, {condition}")
    elif response.status_code == 401:
        print("❌ Invalid API key. Please check your key or regenerate it on OpenWeatherMap.")
    else:
        print(f"⚠️ API returned status {response.status_code}: {data.get('message')}")
except Exception as e:
    print(f"⚠️ Exception occurred: {e}")
