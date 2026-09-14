"""
Daily Air Quality Action Agent — Dashboard
Calls a Langflow flow (AQI Data Agent -> Health Advisory Agent ->
Forecasting Agent -> Community Action Agent) and visualizes the result.

Run with: streamlit run dashboard.py
"""

import requests
import streamlit as st

# ---- Config ----
LANGFLOW_BASE_URL = "http://localhost:7860"
FLOW_ID = "afb2f9d7-f874-4ad1-b2c1-35af32db48c8"
LANGFLOW_API_KEY = "sk-Ew-QzFbIcv2cpd9euR2S5ImnAYbdhdRm_gF1LybfQks"

st.set_page_config(page_title="Air Quality Action Agent", layout="wide")
st.title("🌫️ Daily Air Quality Action Agent")

with st.sidebar:
    st.header("Your profile")
    city = st.text_input("City", "chennai")
    age = st.number_input("Age", min_value=1, max_value=120, value=25)
    condition = st.selectbox(
        "Health condition",
        ["None", "Asthma", "Heart condition", "Pregnant", "Elderly (65+)", "Child (under 12)"],
    )
    run = st.button("Get today's air quality plan", type="primary")


def call_langflow(city: str, age: int, condition: str) -> list:
    url = f"{LANGFLOW_BASE_URL}/api/v1/run/{FLOW_ID}"
    headers = {"Content-Type": "application/json", "x-api-key": LANGFLOW_API_KEY}
    payload = {
        "input_value": f"City: {city}. Age: {age}. Condition: {condition}.",
        "output_type": "chat",
        "input_type": "chat",
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=90)
    resp.raise_for_status()
    data = resp.json()

    texts = []
    for out in data["outputs"][0]["outputs"]:
        try:
            texts.append(out["results"]["message"]["text"])
        except (KeyError, TypeError):
            continue
    return texts


if run:
    with st.spinner("Fetching AQI data and running the agent chain..."):
        try:
            results = call_langflow(city, age, condition)
        except Exception as e:
            st.error(f"Could not reach the Langflow flow: {e}")
            st.stop()

    labels = ["🏥 Health Advisory", "📈 Forecast Alert", "🤝 Community Action"]
    st.subheader("Your personalized air quality plan")
    for i, text in enumerate(results):
        label = labels[i] if i < len(labels) else f"Agent {i+1}"
        st.markdown(f"**{label}**")
        st.write(text)
        st.divider()

else:
    st.info("Enter your details in the sidebar and click **Get today's air quality plan**.")
