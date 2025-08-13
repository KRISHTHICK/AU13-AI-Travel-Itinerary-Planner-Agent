from haversine import haversine

def total_route_distance_km(route):
    if len(route) < 2: return 0.0
    dist = 0.0
    for i in range(len(route)-1):
        a = (route[i]["lat"], route[i]["lon"])
        b = (route[i+1]["lat"], route[i+1]["lon"])
        dist += haversine(a, b)
    return dist
