import streamlit as st
import pandas as pd
from pydeck import Deck, Layer, ViewState
import requests

st.set_page_config(
    page_title="Alzheimer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Create a function to search for nearby doctors based on city name
@st.cache_data
def search_doctors(city: str):
    # Google Maps API key
    api_key = st.secrets["API_KEY"]
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=doctors+specializing+in+Alzheimer+in+{city}&key={api_key}"
    results = requests.get(url, timeout=10).json()
    return results["results"]


st.title("Find a doctor near you")

# Input city name
city = st.text_input("Enter city name: ")

if city:
    # Search for nearby doctors
    doctors = search_doctors(city)

    # Display the results to the user
    st.markdown(f"Results for Alzheimer doctors in: {city}")
    lat_long = [
        (doc["geometry"]["location"]["lat"], doc["geometry"]["location"]["lng"])
        for doc in doctors
    ]
    df = pd.DataFrame(lat_long, columns=["latitude", "longitude"])
    st.pydeck_chart(
        Deck(
            map_style="mapbox://styles/mapbox/streets-v12",
            initial_view_state=ViewState(
                latitude=df["latitude"].mean(skipna=True),
                longitude=df["longitude"].mean(skipna=True),
                zoom=11,
                pitch=50,
            ),
            layers=[
                Layer(
                    "ScatterplotLayer",
                    data=df,
                    get_position=["longitude", "latitude"],
                    get_radius=100,
                    get_color=[200, 30, 0],
                    pickable=True,
                    auto_highlight=True,
                )
            ],
        )
    )

    for i, doctor in enumerate(doctors, start=1):
        st.markdown(f"{i}. **Name**: {doctor['name']}")
        st.markdown("> **Address**: {doctor['formatted_address']}")
