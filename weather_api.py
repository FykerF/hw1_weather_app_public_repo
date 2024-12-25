import requests
import time

# Fetch current temperature
def get_current_temperature(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['main']['temp']
    else:
        raise ValueError(response.json()['message'])

# Fetch historical temperatures
def get_historical_temperature(city_name, lat, lon, start_date, end_date, api_key):
    historical_data = []
    start_timestamp = int(time.mktime(time.strptime(start_date, "%Y-%m-%d")))
    end_timestamp = int(time.mktime(time.strptime(end_date, "%Y-%m-%d")))
    
    for timestamp in range(start_timestamp, end_timestamp + 1, 86400):
        url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&appid={api_key}&units=metric"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            temp = data['current']['temp']
            historical_data.append({"city": city_name, "date": time.strftime("%Y-%m-%d", time.gmtime(timestamp)), "temperature": temp})
        else:
            print(f"Error: {response.json()['message']}")
    
    return historical_data
