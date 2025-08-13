def estimate_cost(days, hotel_per_night=80, food_per_day=35, transit_per_day=12, attractions_per_day=25):
    return days*food_per_day + days*transit_per_day + days*attractions_per_day + (days-1)*hotel_per_night

def adjust_for_budget(estimate, budget):
    if not budget: return estimate, "standard"
    if estimate <= budget*0.9: return estimate, "under"
    if estimate <= budget*1.1: return estimate, "on-target"
    return estimate, "over"

def per_day_breakdown(days, hotel_per_night=80, food=35, transit=12, attractions=25):
    out = []
    for d in range(1, days+1):
        day_cost = food + transit + attractions + (hotel_per_night if d < days else 0)
        out.append({"day": d, "estimate": day_cost})
    return out
