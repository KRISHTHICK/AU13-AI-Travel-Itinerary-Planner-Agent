from utils.weather import city_to_latlon, forecast_5day, short_weather_blurb
from utils.places import find_spots, order_greedy
from utils.events import find_events, short_events_blurb
from utils.llm import generate_trip_intro, generate_day_plan, generate_trip_summary
from utils.costs import estimate_cost, adjust_for_budget, per_day_breakdown
from utils.geo import total_route_distance_km

def plan_itinerary(city:str, days:int, interests:list, budget:int|None):
    lat, lon, cc = city_to_latlon(city)
    forecast = forecast_5day(lat, lon)
    weather_blurb = short_weather_blurb(forecast)
    events = find_events(city, cc)
    events_blurb = short_events_blurb(events)

    spots = find_spots(city, lat, lon, interests, limit=max(16, days*4))
    routes = order_greedy(lat, lon, spots, per_day=4, days=days)

    day_weather = [f"{forecast[min(i, len(forecast)-1)]['desc']} around {forecast[min(i, len(forecast)-1)]['temp_c']:.0f}°C" for i in range(days)]

    total_cost = estimate_cost(days)
    total_cost, budget_status = adjust_for_budget(total_cost, budget)
    day_costs = per_day_breakdown(days)

    intro = generate_trip_intro(city, days, ", ".join(interests), weather_blurb, events_blurb)
    day_plans, day_routes_km = [], []
    for i, day_spots in enumerate(routes, start=1):
        plan = generate_day_plan(city, i, day_spots, day_weather[i-1] if i-1 < len(day_weather) else "")
        day_plans.append(plan)
        day_routes_km.append(total_route_distance_km(day_spots))

    themes = ", ".join(sorted(set([s.get("category","explore") for s in spots])))
    summary = generate_trip_summary(city, total_cost, themes)

    return {
        "meta": {"city": city, "days": days, "lat": lat, "lon": lon, "budget": budget, "budget_status": budget_status},
        "weather": forecast,
        "events": events,
        "intro": intro,
        "itinerary": [
            {
                "day": i+1,
                "spots": routes[i],
                "route_km": day_routes_km[i],
                "plan": day_plans[i],
                "cost_estimate": day_costs[i]["estimate"] if i < len(day_costs) else None
            } for i in range(len(routes))
        ],
        "total_cost_estimate": total_cost,
        "summary_bullets": summary
    }
