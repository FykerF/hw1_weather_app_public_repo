import pandas as pd
import numpy as np
from multiprocessing import Pool, cpu_count

#function to calculate rolling statistics
def compute_rolling_stats(city_data, window=30):
    city_data['rolling_mean'] = city_data['temperature'].rolling(window=window).mean()
    city_data['rolling_std'] = city_data['temperature'].rolling(window=window).std()
    return city_data

#function to detect anomalies
def detect_anomalies(city_data):
    city_data['anomaly'] = (abs(city_data['temperature'] - city_data['rolling_mean']) > 2 * city_data['rolling_std']).astype(int)
    return city_data

#process single city data for parallelization
def process_city(city, data):
    city_data = data[data['city'] == city].copy()
    city_data = compute_rolling_stats(city_data)
    city_data = detect_anomalies(city_data)
    return city_data

#parallelized analysis
def parallel_analysis(data):
    cities = data['city'].unique()
    with Pool(cpu_count()) as pool:
        results = pool.starmap(process_city, [(city, data) for city in cities])
    return pd.concat(results)
