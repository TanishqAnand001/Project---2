import pandas as pd

# Load 10-year daily climate data
climate_df = pd.read_csv('../data/tn_climate_10years_daily.csv')
climate_df['date'] = pd.to_datetime(climate_df['date'])

# Calculate seasonal averages for each year
seasonal_data = climate_df.groupby(['District', 'year', 'Season']).agg({
    'temp_mean': 'mean',
    'temp_max': 'max',
    'temp_min': 'min',
    'humidity': 'mean',
    'rainfall': 'sum'
}).reset_index()

seasonal_data.rename(columns={
    'temp_mean': 'temperature',
    'temp_max': 'temperature_max',
    'temp_min': 'temperature_min',
    'humidity': 'humidity',
    'rainfall': 'rainfall'
}, inplace=True)

# Round values
seasonal_data['temperature'] = seasonal_data['temperature'].round(1)
seasonal_data['temperature_max'] = seasonal_data['temperature_max'].round(1)
seasonal_data['temperature_min'] = seasonal_data['temperature_min'].round(1)
seasonal_data['humidity'] = seasonal_data['humidity'].round(1)
seasonal_data['rainfall'] = seasonal_data['rainfall'].round(0)

# Save
seasonal_data.to_csv('../data/tn_climate_10years_seasonal.csv', index=False)

print(f"✅ Seasonal aggregates created!")
print(f"Total rows: {len(seasonal_data)}")
print(f"Districts: {seasonal_data['District'].nunique()}")
print(f"Years: {seasonal_data['year'].min()} - {seasonal_data['year'].max()}")
print(f"\nSample:\n{seasonal_data.head(10)}")
