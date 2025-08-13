import os
import requests

TM_KEY = os.getenv("TICKETMASTER_API_KEY")

def find_events(city, country_code=None, size=10):
    if not TM_KEY:
        return [{"name":"City Live Concert","date":"Sat Evening","venue":"Main Arena"}]
    params = {"apikey": TM_KEY, "city": city, "size": str(size), "sort": "date,asc"}
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    events = []
    for ev in data.get("_embedded", {}).get("events", []):
        events.append({
            "name": ev.get("name"),
            "date": ev.get("dates", {}).get("start", {}).get("localDate", ""),
            "venue": (ev.get("_embedded", {}).get("venues",[{}])[0].get("name",""))
        })
    return events[:size]

def short_events_blurb(events):
    if not events: return "No notable events found."
    tops = events[:3]
    return "; ".join([f"{e['name']} ({e['date']})" for e in tops])
