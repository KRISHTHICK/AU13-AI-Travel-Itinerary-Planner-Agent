# AU13-AI-Travel-Itinerary-Planner-Agent
Ai Agent
Idea:
An AI agent that plans a personalized travel itinerary for any destination based on user preferences (budget, interests, travel dates, food preferences).
It can:

Take input like destination, duration, interests (beaches, adventure, culture), and budget.

Fetch real-time weather and events at that location.

Suggest places to visit, restaurants, and activities day-by-day.

Provide a cost estimate and optimized route order.

Allow the user to regenerate or tweak the plan instantly.

Why Agent?

The LLM alone can suggest places, but the agent integrates multiple tools:

Weather API

Events API

Google Places API

LLM summarization

Cost estimation calculator

The agent coordinates these tools automatically in a chain of actions.

Example Flow:

markdown
Copy
Edit
User: "Plan a 5-day trip to Tokyo for under $1000, I love anime and street food."
Agent:
  1. Fetches weather forecast for Tokyo in the given dates.  
  2. Checks upcoming anime events & festivals.  
  3. Finds famous street food spots.  
  4. Optimizes daily travel route.  
  5. Summarizes in a neat itinerary + cost breakdown.

# 🧭 AI Travel Itinerary Planner Agent

Plan a personalized trip with real-time **weather**, **events**, **places**, route optimization and **LLM** write-ups.  
Works with **OpenAI** or **Ollama (local)**, and supports **Demo mode** (no API keys).

## Features
- City geocoding → 5-day weather forecast (OpenWeather)
- POIs by interests (OpenTripMap)
- Events (Ticketmaster)
- Greedy route per day + distance
- Cost estimates & budget status
- LLM write-ups (intro, per-day plan, 5-bullet summary)
- **Map thumbnails** (Google Static Maps, optional)
- **Export** JSON and CSV

## Quickstart
```bash
git clone <this-repo>
cd travel-itinerary-agent
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # fill keys if you have them (optional)
streamlit run app.py


.env keys (optional)
PROVIDER=openai|ollama|none

OPENAI_API_KEY, OPENAI_MODEL

OLLAMA_BASE_URL, OLLAMA_MODEL

OPENWEATHER_API_KEY

OPENTRIPMAP_API_KEY

TICKETMASTER_API_KEY

GOOGLE_MAPS_STATIC_API_KEY (for map thumbnails)

If you set PROVIDER=none, the app uses a small built-in summarizer.

Notes
POIs: OpenTripMap free tier is fine for demos.

Events: Ticketmaster Discovery API (free key).

Weather: OpenWeather 5-day forecast.

Routing: Greedy nearest neighbor (fast & simple). You can swap with OR-Tools later.

yaml
Copy
Edit

---

## 🧹 .gitignore

```gitignore
# Python
__pycache__/
*.pyc
.venv/
.env

# Streamlit
.streamlit/

# OS
.DS_Store
Thumbs.db
📄 LICENSE (MIT)
txt
Copy
Edit
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
...
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND...
▶️ Run
bash
Copy
Edit
pip install -r requirements.txt
cp .env.example .env   # (optional) add keys or leave empty for Demo mode
streamlit run app.py
