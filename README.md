Features
Upload Raw Temperature Data:

Upload a CSV file containing historical temperature data.
The file must include the following columns:
timestamp (Date of measurement, in a parseable format like YYYY-MM-DD).
temperature (Daily average temperature in °C).
city (Name of the city).
Data is dynamically processed to compute rolling statistics and detect anomalies.
City-Specific Analysis:

Select a city from the dropdown menu to:
View historical temperature trends.
Identify anomalies (temperatures exceeding mean ± 2σ).
Real-Time Temperature Monitoring:

Enter an OpenWeatherMap API key to fetch the current temperature for the selected city.
Compare the real-time temperature to historical norms for the same season.
Interactive Interface:

Built with Streamlit for an easy-to-use and responsive interface.

License 

This project is licensed under the MIT License. See the LICENSE file for more details.
