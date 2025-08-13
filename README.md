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
