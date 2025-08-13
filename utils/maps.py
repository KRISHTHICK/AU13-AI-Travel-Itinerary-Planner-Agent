#(optional thumbnails)
import os
from urllib.parse import urlencode

GKEY = os.getenv("GOOGLE_MAPS_STATIC_API_KEY")

def static_map_for_points(points, width=640, height=320, zoom=None):
    """
    points: list of dicts with lat, lon, name.
    If no key configured, returns None.
    """
    if not GKEY or not points:
        return None
    center_lat = sum(p["lat"] for p in points)/len(points)
    center_lon = sum(p["lon"] for p in points)/len(points)
    base = "https://maps.googleapis.com/maps/api/staticmap"
    markers = []
    for p in points:
        markers.append(f"size:mid|{p['lat']},{p['lon']}")
    params = {
        "size": f"{width}x{height}",
        "scale": 2,
        "maptype": "roadmap",
        "key": GKEY,
        "center": f"{center_lat},{center_lon}",
    }
    if zoom:
        params["zoom"] = int(zoom)
    qs = urlencode(params)
    marker_params = "&".join([f"markers={m}" for m in markers])
    return f"{base}?{qs}&{marker_params}"
