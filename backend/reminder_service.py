from dotenv import load_dotenv
import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import time
from notifications import add_notification  # your notifications.py

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OWM_API_KEY")
print(f"API Key loaded: '{API_KEY}'")

# Scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# ===== Weather Function =====
def get_weather(city="Chennai"):
    if not API_KEY:
        print("⚠️ API key missing. Skipping weather fetch.")
        return None
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(url, params=params)
        data = response.json()
        if response.status_code != 200:
            print(f"⚠️ Weather API error: {data.get('message', 'Unknown error')}")
            return None
        return data
    except Exception as e:
        print(f"⚠️ Exception fetching weather: {e}")
        return None

# ===== Jobs =====
def weather_based_alert():
    weather = get_weather()
    if weather:
        temp = weather['main']['temp']
        condition = weather['weather'][0]['description']
        message = f"{temp}°C, {condition}"
        print(f"🌤 Weather Alert: {message}")
        add_notification("Weather Alert", message)
    else:
        print("Skipping weather alert due to missing/invalid API key.")

def crop_reminder():
    message = "Check your crops today!"
    print(f"🌱 {message}")
    add_notification("Crop Reminder", message)

def scheme_reminder():
    message = "Apply for subsidy scheme before deadline!"
    print(f"📅 {message}")
    add_notification("Scheme Reminder", message)

def market_price_alert():
    price = 1500  # Example; replace with real market API
    message = f"Wheat price is ₹{price}/quintal"
    print(f"💰 {message}")
    add_notification("Market Price Alert", message)

# ===== Schedule Jobs =====
scheduler.add_job(crop_reminder, 'interval', minutes=1)
scheduler.add_job(scheme_reminder, 'interval', hours=6)
scheduler.add_job(market_price_alert, 'interval', hours=3)

if API_KEY:
    scheduler.add_job(weather_based_alert, 'interval', minutes=5)
else:
    print("Weather job not scheduled because API key is missing.")

# ===== Add initial notifications immediately =====
crop_reminder()
scheme_reminder()
market_price_alert()
if API_KEY:
    weather_based_alert()

# ===== Keep Script Running =====
try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
