import streamlit as st
import pandas as pd
from main_analysis import parallel_analysis
from weather_api import get_current_temperature

# Cache processed data
@st.cache_data
def process_data(raw_data):
    # Process raw data using parallel analysis
    processed_data = parallel_analysis(raw_data)
    return processed_data

def main():
    st.title("Temperature Analysis and Monitoring")

    # Step 1: Upload raw data
    uploaded_file = st.file_uploader("Upload raw temperature data (CSV)", type=["csv"])
    if not uploaded_file:
        st.warning("Please upload a CSV file to proceed.")
        return  # Stop further execution if no file is uploaded

    # Step 2: Load and display the uploaded file
    try:
        raw_data = pd.read_csv(uploaded_file, parse_dates=['timestamp'])
        st.success("File uploaded and loaded successfully!")
        st.write("Raw Data Preview:")
        st.dataframe(raw_data.head())
    except Exception as e:
        st.error(f"Error loading the uploaded file: {e}")
        return

    # Step 3: Process raw data
    with st.spinner("Processing data..."):
        try:
            processed_data = process_data(raw_data)
            st.success("Data processing complete!")
        except Exception as e:
            st.error(f"Error processing the data: {e}")
            return

    # Step 4: City selection and display analysis
    city = st.selectbox("Select a city", processed_data['city'].unique())
    city_data = processed_data[processed_data['city'] == city]

    st.write(f"Temperature trends for {city}")
    st.line_chart(city_data[['timestamp', 'temperature']].set_index('timestamp'))

    anomalies = city_data[city_data['anomaly'] == 1]
    st.write("Temperature anomalies:")
    st.dataframe(anomalies)

    # Step 5: OpenWeatherMap API for current temperature
    api_key = st.text_input("Enter your OpenWeatherMap API key", type="password")
    if api_key:
        try:
            st.write(f"Fetching current temperature for {city}...")
            current_temp = get_current_temperature(city, api_key)

            # Calculate anomaly
            season = city_data['season'].iloc[-1]
            normal_range = city_data[city_data['season'] == season]['temperature'].agg(['mean', 'std'])
            lower_bound = normal_range['mean'] - 2 * normal_range['std']
            upper_bound = normal_range['mean'] + 2 * normal_range['std']

            st.write(f"Current temperature in {city}: {current_temp}°C")
            st.write(f"Normal range for {season}: {lower_bound:.2f}°C to {upper_bound:.2f}°C")
            st.write(
                "The current temperature is **anomalous!**"
                if not (lower_bound <= current_temp <= upper_bound)
                else "The current temperature is within the normal range."
            )
        except ValueError as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
