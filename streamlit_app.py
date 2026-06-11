import streamlit as st
import requests

st.set_page_config(
    page_title="Car Price Predictor",
    layout="centered"
)

st.title("🚗 Car Price Prediction")

name = st.text_input("Car Name")

year = st.number_input(
    "Year",
    min_value=1990,
    max_value=2035,
    value=2015
)

km_driven = st.number_input(
    "KM Driven",
    min_value=0,
    value=50000
)

fuel = st.selectbox(
    "Fuel Type",
    ["Petrol", "Diesel", "CNG", "LPG", "Electric"]
)

seller_type = st.selectbox(
    "Seller Type",
    ["Individual", "Dealer", "Trustmark Dealer"]
)

transmission = st.selectbox(
    "Transmission",
    ["Manual", "Automatic"]
)

owner = st.selectbox(
    "Owner",
    [
        "First Owner",
        "Second Owner",
        "Third Owner",
        "Fourth & Above Owner",
        "Test Drive Car"
    ]
)

if st.button("Predict Price"):

    payload = {
        "name": name,
        "year": int(year),
        "km_driven": int(km_driven),
        "fuel": fuel,
        "seller_type": seller_type,
        "transmission": transmission,
        "owner": owner
    }

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=payload
    )

    if response.status_code == 200:
        price = response.json()["predicted_price"]

        st.success(
            f"Estimated Car Price: ₹ {price:,.0f}"
        )

    else:
        st.error("Prediction Failed")