import os
import requests
from datetime import datetime
from collections import defaultdict

OW_KEY = os.getenv("OPENWEATHER_API_KEY")

def city_to_latlon(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    data = r.json()
    if data.get("results"):
        res = data["results"][0]
        return res["latitude"], res["longitude"], res.get("country_code","")
    raise ValueError("City not found")

def forecast_5day(lat, lon):
    if not OW_KEY:
        return [{"date": f"Day {i+1}", "temp_c": 24 + i, "desc": "Partly cloudy"} for i in range(5)]
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OW_KEY}&units=metric"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    data = r.json()
    buckets = defaultdict(list)
    for block in data.get("list", []):
        dt = datetime.fromtimestamp(block["dt"])
        day = dt.strftime("%Y-%m-%d")
        buckets[day].append(block)
    out = []
    for day, arr in list(buckets.items())[:5]:
        temps = [x["main"]["temp"] for x in arr]
        desc = arr[0]["weather"][0]["description"].title()
        out.append({"date": day, "temp_c": sum(temps)/len(temps), "desc": desc})
    return out

def short_weather_blurb(forecast):
    parts = [f"{d['date']}: {d['temp_c']:.0f}°C, {d['desc']}" for d in forecast]
    return "; ".join(parts[:3]) + ("..." if len(parts) > 3 else "")
