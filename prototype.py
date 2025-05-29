import pandas as pd
import streamlit as st
import requests
import folium

st.title("Climate Health Dashboard")

#to create this dashboard with both static and real-time data, I first had to download the zipcode dataset and define
#the reference path to the dataset in my local drive.
zip_code_data = pd.read_csv("/Users/nastemko/Documents/Climatehealthappdata/simplemaps_uszips_basicv1.90")  # Or your file path

zip_code_input = st.text_input("Enter ZIP Code:")

#Here there is an expectation that a user will type in a valid zip code.
if zip_code_input:
    location_info = get_location_data(zip_code_input, zip_code_data)
    if location_info:
        #... (your API calls and data display)
    else:
        st.write("Invalid ZIP code.")
else:
    st.write("Please enter a ZIP code.")


#Fucking it up by defining the next step. I need to set the NOAA API key to have this program load the hourly forecast


# --- API Keys (Replace with your actual keys) ---
OPENWEATHERMAP_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
AIRNOW_API_KEY = "YOUR_AIRNOW_API_KEY"
# -----------------------------------------------

# Load ZIP code data
zip_code_data = pd.read_csv("uszips.csv")  # Or your file path

# Function to get location data (lat, lng, county)
def get_location_data(zip_code, zip_code_data):
    try:
        zip_code = int(zip_code)  # Convert to integer for matching
        location_data = zip_code_data[zip_code_data['zip'] == zip_code].iloc
        return {
            "lat": location_data['lat'],
            "lng": location_data['lng'],
            "county": location_data['county_name']  # Adjust column name if needed
        }
    except IndexError:
        return None

        import requests

        def get_forecast(lat, lon):
            try:
                # 1. Get gridpoint information
                points_url = f"https://api.weather.gov/points/{lat},{lon}"
                points_response = requests.get(points_url)
                points_data = points_response.json()

                # 2. Extract forecast link (hourly in this example)
                forecast_url = points_data['properties']['forecastHourly']

                # 3. Get the forecast
                forecast_response = requests.get(forecast_url)
                forecast_data = forecast_response.json()

                # ... (process forecast_data to extract temperature and humidity)

                return temperature, humidity

            except Exception as e:
                print(f"Error fetching forecast: {e}")
                return None

        # --- Heat Index Calculation (using Rothfusz regression) ---
        # (You'll need to implement this calculation or find a library)
        # For now, let's use a placeholder:
        heat_index = temperature_f + humidity  # Placeholder calculation
        # ---------------------------------------------------------

        return heat_index
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

# Function to get AQI (using AirNow API)
def get_aqi(lat, lon, api_key=AIRNOW_API_KEY):
    try:
        url = f"http://www.airnowapi.org/aq/observation/latLong/current/?format=application/json&latitude={lat}&longitude={lon}&distance=25&API_KEY={api_key}"
        response = requests.get(url)
        data = response.json()
        aqi = data['AQI']  # Assuming the first entry is the most relevant
        return aqi
    except Exception as e:
        print(f"Error fetching AQI data: {e}")
        return None

# --- Streamlit App ---
st.title("Climate Health App")

zip_code_input = st.text_input("Enter ZIP Code:")

if zip_code_input:
    location_info = get_location_data(zip_code_input, zip_code_data)
    if location_info:
        heat_index = get_heat_index(location_info["lat"], location_info["lng"])
        aqi = get_aqi(location_info["lat"], location_info["lng"])

        st.write(f"Heat Index: {heat_index}")
        st.write(f"AQI: {aqi}")
    else:
        st.write("Invalid ZIP code.")
else:
    st.write("Please enter a ZIP code.")