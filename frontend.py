import streamlit as st
import requests

st.title("🌾 Crop Predictor")
st.markdown("Enter your soil and weather details below:")

API_URL = "http://127.0.0.1:8000/predict"

# Inputs
nitrogen = st.number_input('Amount of Nitrogen in soil', min_value=1, max_value=500, value=36)
phosphorus = st.number_input('Amount of Phosphorus in soil', min_value=1, max_value=500, value=32)
potassium = st.number_input('Amount of Potassium in soil', min_value=1, max_value=500, value=50)
temperature = st.number_input('Temperature in area (°C)', min_value=1, max_value=500, value=5)
humidity = st.number_input('Humidity in air (%)', min_value=1, max_value=500, value=70)
ph = st.number_input('pH of soil', min_value=1, max_value=500, value=3)
rainfall = st.number_input('Rainfall in area (mm)', min_value=1, max_value=500, value=200)

if st.button('Predict Crop'):
    input_data = {
        'Nitrogen': nitrogen,
        'Phosphorus': phosphorus,
        'Potassium': potassium,
        'Temperature': temperature,
        'Humidity': humidity,  # ✅ Fixed casing: was 'humidity'
        'PH': ph,
        'Rainfall': rainfall
    }

    try:
        response = requests.post(API_URL, json=input_data)

        # ✅ Handle failed requests
        if response.status_code != 200:
            st.error(f"🚫 API Error {response.status_code}: {response.text}")
        else:
            result = response.json()

            # ✅ Check if key exists
            if 'predicted_category' in result:
                st.success(f"✅ Predicted Crop: **{result['predicted_category']}**")
            else:
                st.error("⚠️ Response does not contain 'predicted_category'.")

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to FastAPI backend. Make sure it's running.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
