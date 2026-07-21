import streamlit as st
import requests

st.set_page_config(
    page_title="California House Price Prediction",
    page_icon="🏡",
    layout="wide"
)


## INPUT FROM USER  ##
st.sidebar.header("Enter House Information")

age = st.sidebar.slider(
    "Housing Median Age",
    min_value=1,
    max_value=60,
    value=25
)

total_rooms = st.sidebar.number_input(
    "Total Rooms",
    min_value=1,
    value=2000
)

total_bedrooms = st.sidebar.number_input(
    "Total Bedrooms",
    min_value=1,
    value=400
)

population = st.sidebar.number_input(
    "Population",
    min_value=1,
    value=1500
)

households = st.sidebar.number_input(
    "Households",
    min_value=1,
    value=350
)

median_income = st.sidebar.slider(
    "Median Income",
    min_value=0.5,
    max_value=15.0,
    value=4.0,
    step=0.1
)

ocean_proximity = st.sidebar.selectbox(
    "Ocean Proximity",
    [
        "<1H OCEAN",
        "INLAND",
        "ISLAND",
        "NEAR BAY",
        "NEAR OCEAN"
    ]
)

## PREPARE the data for model
payload = {'housing_median_age':age,
            'total_rooms':total_rooms,
            'total_bedrooms':total_bedrooms,
            'population':population,
            'households':households, #np.nan
            'median_income':median_income,
            'ocean_proximity':ocean_proximity}


if st.button("احسب السعر"):
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)        
        if response.status_code == 200:
            result = response.json()
            st.success(f"السعر المتوقع من الـ API: ${result['prediction']:,.2f}")
        else:
            st.error("حدث خطأ في خادم الباك إند.")
    except Exception as e:
        st.error(f"تعذر الاتصال بالـ API: {e}")