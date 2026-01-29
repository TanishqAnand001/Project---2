import pandas as pd
import os

project_root = r'C:\Users\acer\PycharmProjects\Project---2'

# Load your original daily climate data
daily_climate_path = os.path.join(project_root, 'data', 'tn_climate_10years_daily.csv')
daily_df = pd.read_csv(daily_climate_path)

# Convert date to datetime
daily_df['date'] = pd.to_datetime(daily_df['date'])

# Extract year and month
daily_df['year'] = daily_df['date'].dt.year
daily_df['month'] = daily_df['date'].dt.month

# Monthly aggregation
monthly_df = daily_df.groupby(['District', 'year', 'month']).agg({
    'temperature': 'mean',
    'temperature_max': 'max',
    'temperature_min': 'min',
    'humidity': 'mean',
    'rainfall': 'sum',  # Total monthly rainfall
    'wind_speed': 'mean'
}).reset_index()

# Add month name for readability
month_names = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}
monthly_df['month_name'] = monthly_df['month'].map(month_names)

# Save monthly climate data
output_path = os.path.join(project_root, 'data', 'tn_climate_monthly.csv')
monthly_df.to_csv(output_path, index=False)

print(f"✅ Monthly climate data created!")
print(f"Total monthly records: {len(monthly_df)}")
print(f"\nSample:\n{monthly_df.head()}")
