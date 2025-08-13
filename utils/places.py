import os
import requests
from math import radians, sin, cos, sqrt, atan2

OTM_KEY = os.getenv("OPENTRIPMAP_API_KEY")

def _dist_km(a, b):
    R = 6371.0
    lat1, lon1 = radians(a[0]), radians(a[1])
    lat2, lon2 = radians(b[0]), radians(b[1])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    h = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return R * 2 * atan2(sqrt(h), sqrt(1-h))

def city_bbox(lat, lon, km=10):
    d = km / 111.0
    return lat-d, lon-d, lat+d, lon+d

def find_spots(city, lat, lon, interests, limit=25):
    if not OTM_KEY:
        demo = [
            {"name": "Central Market", "lat": lat+0.01, "lon": lon+0.01, "category": "food"},
            {"name": "Old Town Museum", "lat": lat+0.015, "lon": lon-0.012, "category": "culture"},
            {"name": "Riverside Walk", "lat": lat-0.009, "lon": lon+0.008, "category": "scenic"},
            {"name": "Theme Street", "lat": lat-0.014, "lon": lon-0.004, "category": "shopping"},
            {"name": "City Viewpoint", "lat": lat+0.02, "lon": lon+0.002, "category": "view"},
            {"name": "Tech Mall", "lat": lat-0.012, "lon": lon+0.016, "category": "shopping"},
            {"name": "Harbor Promenade", "lat": lat+0.006, "lon": lon-0.018, "category": "scenic"},
            {"name": "Local Izakaya Alley", "lat": lat-0.017, "lon": lon+0.006, "category": "food"},
        ]
        return demo[:limit]

    kinds_map = {
        "culture": "museums,monuments,heritage,architecture,cultural",
        "food": "foods,restaurants,cafes",
        "nature": "natural,parks,gardens,view_points",
        "shopping": "shopping,malls,markets",
        "adventure": "sport,amusements,theme_parks",
        "scenic": "view_points,urban_environment,interesting_places",
        "anime": "museums,cinemas,amusements"
    }
    kinds = []
    for k in interests:
        kinds.extend(kinds_map.get(k.lower(), "interesting_places").split(","))
    kinds = ",".join(sorted(set(kinds)))
    lat_min, lon_min, lat_max, lon_max = city_bbox(lat, lon, km=10)
    url = ("https://api.opentripmap.com/0.1/en/places/bbox"
           f"?lon_min={lon_min}&lat_min={lat_min}&lon_max={lon_max}&lat_max={lat_max}"
           f"&kinds={kinds}&limit={limit}&format=json&apikey={OTM_KEY}")
    r = requests.get(url, timeout=25)
    r.raise_for_status()
    results = r.json()
    out = []
    for p in results:
        out.append({
            "name": p.get("name") or p.get("kinds","POI").split(",")[0].title(),
            "lat": p["point"]["lat"],
            "lon": p["point"]["lon"],
            "category": (p.get("kinds","other").split(",")[0])
        })
    return out

def order_greedy(start_lat, start_lon, spots, per_day=4, days=3):
    remaining = spots[:]
    days_list = []
    start = (start_lat, start_lon)
    for _ in range(days):
        if not remaining: break
        day_route, cur = [], start
        for _ in range(min(per_day, len(remaining))):
            nxt_idx, nxt_d = None, 1e9
            for i, s in enumerate(remaining):
                d = _dist_km(cur, (s["lat"], s["lon"]))
                if d < nxt_d:
                    nxt_d, nxt_idx = d, i
            s = remaining.pop(nxt_idx)
            day_route.append(s)
            cur = (s["lat"], s["lon"])
        days_list.append(day_route)
    return days_list
