#(Streamlit UI with map + CSV export)
import os
import json
import io
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from agent.itinerary_agent import plan_itinerary
from utils.maps import static_map_for_points

load_dotenv()

st.set_page_config(page_title="AI Travel Itinerary Agent", layout="wide")
st.title("🧭 AI Travel Itinerary Planner Agent")

with st.sidebar:
    st.header("Trip Inputs")
    city = st.text_input("Destination City", value="Tokyo")
    days = st.number_input("Days", min_value=1, max_value=14, value=5)
    budget = st.number_input("Budget (USD, optional)", min_value=0, value=1000, step=50)
    interests = st.multiselect(
        "Interests",
        ["culture", "food", "nature", "shopping", "adventure", "scenic", "anime"],
        default=["food", "culture", "scenic"]
    )
    st.caption(f"LLM Provider: {os.getenv('PROVIDER','none')} (set in .env)")
run = st.button("Plan Trip")

def spots_to_csv_bytes(days_data):
    # Flatten for CSV download
    rows = []
    for day in days_data:
        d = day["day"]
        for s in day["spots"]:
            rows.append({"day": d, "name": s["name"], "category": s.get("category",""), "lat": s["lat"], "lon": s["lon"]})
    df = pd.DataFrame(rows)
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue().encode("utf-8")

if run:
    with st.spinner("Planning your itinerary..."):
        data = plan_itinerary(city, int(days), interests, int(budget) if budget>0 else None)

    st.success("Itinerary ready!")
    st.subheader("Overview")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("City", data["meta"]["city"])
    with col2: st.metric("Days", data["meta"]["days"])
    with col3: st.metric("Budget Status", data["meta"]["budget_status"].upper())

    st.write("**Intro**")
    st.write(data["intro"])

    c1, c2 = st.columns(2)
    with c1:
        st.write("**Weather (first 5 days)**")
        st.table(pd.DataFrame(data["weather"]))
    with c2:
        st.write("**Top Events**")
        st.table(pd.DataFrame(data["events"]))

    st.write("**Daily Plans**")
    for day in data["itinerary"]:
        with st.expander(f"Day {day['day']} — {day['route_km']:.1f} km route — ~${day['cost_estimate']}"):
            # Map thumbnail if key present
            map_url = static_map_for_points(day["spots"])
            if map_url:
                st.image(map_url, caption="Route area (markers only)", use_container_width=True)
            spots_df = pd.DataFrame(day["spots"])
            st.table(spots_df[["name","category","lat","lon"]])
            st.markdown("**Plan**")
            st.write(day["plan"])

    st.subheader("Budget & Summary")
    st.metric("Total Cost Estimate", f"${data['total_cost_estimate']:.0f}")
    st.markdown("**In 5 bullets:**")
    st.write(data["summary_bullets"])

    # Exports
    st.download_button(
        "⬇️ Download JSON",
        data=json.dumps(data, indent=2),
        file_name=f"itinerary_{data['meta']['city']}_{data['meta']['days']}d.json",
        mime="application/json"
    )
    st.download_button(
        "⬇️ Download Spots CSV",
        data=spots_to_csv_bytes(data["itinerary"]),
        file_name=f"spots_{data['meta']['city']}_{data['meta']['days']}d.csv",
        mime="text/csv"
    )

    st.info("Tip: Add API keys in `.env` for live data and maps. Without keys, the app runs in Demo mode.")
else:
    st.caption("Fill inputs then click **Plan Trip**")
