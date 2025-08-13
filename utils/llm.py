import os
import requests

PROVIDER = os.getenv("PROVIDER", "none").lower()

def _openai_chat(messages, model=None):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    body = {"model": model, "messages": messages, "temperature": 0.3}
    r = requests.post(url, headers=headers, json=body, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def _ollama_chat(messages, model=None):
    base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = model or os.getenv("OLLAMA_MODEL", "llama3.1:8b-instruct")
    url = f"{base}/api/chat"
    payload = {"model": model, "messages": messages, "stream": False}
    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["message"]["content"]

def _fallback_summary(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    head = lines[:8]
    return "• " + "\n• ".join(head) if head else "No content to summarize."

def generate_trip_intro(city, days, prefs, weather_blurb, events_blurb):
    system = {"role": "system", "content": "You are a concise, friendly travel planner."}
    user = {"role": "user", "content": f"""
Create a warm intro (80-120 words) for a {days}-day trip to {city}.
Traveler preferences: {prefs}.
Include 1 line on weather: {weather_blurb}.
Include 1 line on notable events: {events_blurb}.
Avoid repeating days; no headers; no emojis.
"""}
    if PROVIDER == "openai":
        return _openai_chat([system, user])
    elif PROVIDER == "ollama":
        return _ollama_chat([system, user])
    else:
        txt = f"Trip to {city} for {days} days. Prefs: {prefs}. Weather: {weather_blurb}. Events: {events_blurb}."
        return _fallback_summary(txt)

def generate_day_plan(city, day_idx, places, weather_day_summary):
    bullets = "\n".join([f"- {p['name']} ({p.get('category','spot')})" for p in places])
    system = {"role": "system", "content": "You are a precise travel assistant."}
    user = {"role": "user", "content": f"""
Write a short day {day_idx} plan (~80-120 words) for {city}.
Spots to cover (in order): 
{bullets}
Weather: {weather_day_summary}.
Mention approximate time blocks (morning/afternoon/evening). Keep it crisp.
"""}
    if PROVIDER == "openai":
        return _openai_chat([system, user])
    elif PROVIDER == "ollama":
        return _ollama_chat([system, user])
    else:
        return _fallback_summary(f"{city} Day {day_idx}: " + bullets)

def generate_trip_summary(city, total_cost_estimate, themes):
    system = {"role": "system", "content": "You summarize trips crisply in bullets."}
    user = {"role": "user", "content": f"""
Summarize the {city} itinerary in 5 bullets. Include:
- vibe/themes: {themes}
- total budget estimate: ${total_cost_estimate:.0f}
Avoid repetition. Keep each bullet < 20 words.
"""}
    if PROVIDER == "openai":
        return _openai_chat([system, user])
    elif PROVIDER == "ollama":
        return _ollama_chat([system, user])
    else:
        return _fallback_summary(f"{city} themes: {themes}, cost: {total_cost_estimate}")
