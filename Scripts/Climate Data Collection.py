import requests
import pandas as pd
import time
from datetime import datetime

# Tamil Nadu district coordinates
district_coords = {
    'Kancheepuram': (12.8342, 79.7036),
    'Cuddalore': (11.7480, 79.7714),
    'Villupuram': (11.9401, 79.4861),
    'Vellore': (12.9165, 79.1325),
    'Tiruvannamalai': (12.2253, 79.0747),
    'Salem': (11.6643, 78.1460),
    'Namakkal': (11.2189, 78.1677),
    'Dharmapuri': (12.1211, 78.1582),
    'Krishnagiri': (12.5186, 78.2137),
    'Coimbatore': (11.0168, 76.9558),
    'Tiruppur': (11.1085, 77.3411),
    'Erode': (11.3410, 77.7172),
    'Trichy': (10.7905, 78.7047),
    'Perambalur': (11.2324, 78.8837),
    'Ariyalur': (11.1401, 79.0770),
    'Karur': (10.9601, 78.0766),
    'Pudukkottai': (10.3833, 78.8200),
    'Thanjavur': (10.7870, 79.1378),
    'Thiruvarur': (10.7660, 79.6345),
    'Madurai': (9.9252, 78.1198),
    'Theni': (10.0104, 77.4777),
    'Dindigul': (10.3673, 77.9803),
    'Ramanathapuram': (9.3639, 78.8377),
    'Sivagangai': (9.8433, 78.4809),
    'Virudhunagar': (9.5810, 77.9624),
    'Tirunelveli': (8.7139, 77.7567),
    'Tuticorin': (8.8054, 78.1451),
    'Kanyakumari': (8.0883, 77.5385),
    'The Nilgiris': (11.4102, 76.6950)
}


def fetch_climate_data(lat, lon, start_date, end_date):
    """Fetch historical climate data from Open-Meteo API"""
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": [
            "temperature_2m_mean",
            "temperature_2m_max",
            "temperature_2m_min",
            "relative_humidity_2m_mean",
            "precipitation_sum",
            "rain_sum"
        ],
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None


# 10 years of data
start_date = "2020-01-01"
end_date = "2025-12-31"

all_climate_data = []

print("Fetching 5 years of climate data for Tamil Nadu districts...\n")

for district, (lat, lon) in district_coords.items():
    print(f"Fetching data for {district}...")

    max_retries = 3

    for attempt in range(max_retries):
        data = fetch_climate_data(lat, lon, start_date, end_date)

        if data and 'daily' in data:
            daily = data['daily']

            df = pd.DataFrame({
                'date': pd.to_datetime(daily['time']),
                'temp_mean': daily['temperature_2m_mean'],
                'temp_max': daily['temperature_2m_max'],
                'temp_min': daily['temperature_2m_min'],
                'humidity': daily['relative_humidity_2m_mean'],
                'rainfall': daily['precipitation_sum']
            })

            df['District'] = district
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month


            # Define seasons
            def get_season(month):
                if month in [6, 7, 8, 9]:
                    return 'Kharif'
                elif month in [10, 11, 12, 1, 2]:
                    return 'Rabi'
                else:
                    return 'Summer'


            df['Season'] = df['month'].apply(get_season)

            all_climate_data.append(df)
            print(f"  ✅ Success ({len(df)} days)")
            break

        elif attempt < max_retries - 1:
            wait_time = 5 * (2 ** attempt)
            print(f"  ⏳ Retry {attempt + 2}/{max_retries}... waiting {wait_time}s")
            time.sleep(wait_time)
        else:
            print(f"  ❌ Failed after {max_retries} attempts")

    time.sleep(15)

# Combine all data
climate_df = pd.concat(all_climate_data, ignore_index=True)

# Save raw daily data
climate_df.to_csv('../data/tn_climate_10years_daily.csv', index=False)

print(f"\n✅ Raw climate data saved!")
print(f"Total rows: {len(climate_df)}")
print(f"Date range: {climate_df['date'].min()} to {climate_df['date'].max()}")
print(f"\nSample:\n{climate_df.head()}")
