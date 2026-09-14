# Daily Air Quality Action Agent

A multi-agent AI system built in Langflow that turns real-time AQI data into
personalized health guidance, predictive alerts, and community action suggestions.

## Architecture
Chat Input (city, age, health condition)
  -> API Request (WAQI public API - real-time AQI + forecast)
  -> Parser (JSON to text)
  -> 3 parallel agents, each Prompt Template + Gemini Language Model:
       - Health Advisory Agent (personalized recommendations)
       - Forecasting Agent (predicts upcoming risk days, early warnings)
       - Community Action Agent (community-level suggestions)
  -> 3 Chat Outputs

## Files
- `IOC_project.json` - exported Langflow flow, import directly into Langflow
- `dashboard.py` - Streamlit dashboard that calls the flow's API and displays results

## Run it
1. `pip install langflow -U && langflow run`, import IOC_project.json
2. Add your Google (Gemini) API key under Model Providers, and a free WAQI token
   from aqicn.org in the API Request node's URL
3. `pip install streamlit requests`
4. Fill your Flow ID and Langflow API key into dashboard.py
5. `streamlit run dashboard.py`
