import pandas as pd
import numpy as np

# Load your soil data
soil_df = pd.read_csv('../data/average_soil_nutrients_tn_districtwise.csv')

# Tamil Nadu climate data (approximate district-wise averages)
climate_data = {
    'Kancheepuram': {'temperature': 29, 'humidity': 75, 'rainfall': 1200},
    'Cuddalore': {'temperature': 28, 'humidity': 78, 'rainfall': 1150},
    'Villupuram': {'temperature': 29, 'humidity': 72, 'rainfall': 1050},
    'Vellore': {'temperature': 30, 'humidity': 65, 'rainfall': 900},
    'Tiruvannamalai': {'temperature': 28, 'humidity': 68, 'rainfall': 950},
    'Salem': {'temperature': 28, 'humidity': 60, 'rainfall': 850},
    'Namakkal': {'temperature': 29, 'humidity': 62, 'rainfall': 800},
    'Dharmapuri': {'temperature': 27, 'humidity': 65, 'rainfall': 900},
    'Krishnagiri': {'temperature': 26, 'humidity': 68, 'rainfall': 850},
    'Coimbatore': {'temperature': 27, 'humidity': 70, 'rainfall': 700},
    'Tiruppur': {'temperature': 28, 'humidity': 68, 'rainfall': 650},
    'Erode': {'temperature': 29, 'humidity': 65, 'rainfall': 700},
    'Trichy': {'temperature': 30, 'humidity': 70, 'rainfall': 850},
    'Perambalur': {'temperature': 30, 'humidity': 68, 'rainfall': 900},
    'Ariyalur': {'temperature': 30, 'humidity': 65, 'rainfall': 950},
    'Karur': {'temperature': 29, 'humidity': 67, 'rainfall': 750},
    'Pudukkottai': {'temperature': 30, 'humidity': 72, 'rainfall': 900},
    'Thanjavur': {'temperature': 29, 'humidity': 75, 'rainfall': 950},
    'Thiruvarur': {'temperature': 29, 'humidity': 76, 'rainfall': 1100},
    'Madurai': {'temperature': 30, 'humidity': 68, 'rainfall': 850},
    'Theni': {'temperature': 28, 'humidity': 70, 'rainfall': 700},
    'Dindigul': {'temperature': 28, 'humidity': 68, 'rainfall': 900},
    'Ramanathapuram': {'temperature': 30, 'humidity': 74, 'rainfall': 850},
    'Sivagangai': {'temperature': 30, 'humidity': 70, 'rainfall': 900},
    'Virudhunagar': {'temperature': 30, 'humidity': 68, 'rainfall': 850},
    'Tirunelveli': {'temperature': 29, 'humidity': 72, 'rainfall': 700},
    'Tuticorin': {'temperature': 30, 'humidity': 75, 'rainfall': 650},
    'Kanyakumari': {'temperature': 27, 'humidity': 80, 'rainfall': 1400},
    'The Nilgiris': {'temperature': 18, 'humidity': 75, 'rainfall': 1500}
}

# Major crops grown in each district
crop_labels = {
    'Kancheepuram': ['rice', 'groundnut', 'sugarcane'],
    'Cuddalore': ['rice', 'groundnut', 'sugarcane'],
    'Villupuram': ['rice', 'groundnut', 'sugarcane'],
    'Vellore': ['rice', 'groundnut', 'millets'],
    'Tiruvannamalai': ['rice', 'groundnut', 'millets'],
    'Salem': ['rice', 'cotton', 'turmeric'],
    'Namakkal': ['rice', 'cotton', 'tapioca'],
    'Dharmapuri': ['rice', 'millets', 'pulses'],
    'Krishnagiri': ['rice', 'millets', 'vegetables'],
    'Coimbatore': ['cotton', 'maize', 'turmeric'],
    'Tiruppur': ['cotton', 'coconut', 'banana'],
    'Erode': ['turmeric', 'cotton', 'banana'],
    'Trichy': ['rice', 'pulses', 'cotton'],
    'Perambalur': ['rice', 'groundnut', 'cotton'],
    'Ariyalur': ['rice', 'groundnut', 'pulses'],
    'Karur': ['cotton', 'maize', 'banana'],
    'Pudukkottai': ['rice', 'cotton', 'groundnut'],
    'Thanjavur': ['rice', 'sugarcane', 'pulses'],
    'Thiruvarur': ['rice', 'sugarcane', 'groundnut'],
    'Madurai': ['cotton', 'groundnut', 'millets'],
    'Theni': ['cotton', 'banana', 'cardamom'],
    'Dindigul': ['cotton', 'banana', 'vegetables'],
    'Ramanathapuram': ['rice', 'groundnut', 'pulses'],
    'Sivagangai': ['rice', 'cotton', 'groundnut'],
    'Virudhunagar': ['cotton', 'groundnut', 'pulses'],
    'Tirunelveli': ['rice', 'cotton', 'banana'],
    'Tuticorin': ['rice', 'cotton', 'pulses'],
    'Kanyakumari': ['rice', 'coconut', 'rubber'],
    'The Nilgiris': ['tea', 'coffee', 'vegetables']
}

# Create expanded dataset with seasonal variations
expanded_data = []

for _, row in soil_df.iterrows():
    district = row['District']
    climate = climate_data[district]
    crops = crop_labels[district]

    # Create entries for different seasons
    seasons = {
        'Kharif': {'temp_adj': 2, 'humidity_adj': 5, 'rainfall_adj': 400},
        'Rabi': {'temp_adj': -2, 'humidity_adj': -5, 'rainfall_adj': -200},
        'Summer': {'temp_adj': 3, 'humidity_adj': -10, 'rainfall_adj': -300}
    }

    for season, adjustments in seasons.items():
        for crop in crops:
            expanded_data.append({
                'District': district,
                'Season': season,
                'N': row['N_Kg_Ha'],
                'P': row['P_Kg_Ha'],
                'K': row['K_Kg_Ha'],
                'pH': row['pH'],
                'EC': row['EC_dS_m'],
                'OC': row['OC_percent'],
                'S': row['S_ppm'],
                'temperature': climate['temperature'] + adjustments['temp_adj'],
                'humidity': climate['humidity'] + adjustments['humidity_adj'],
                'rainfall': max(0, climate['rainfall'] + adjustments['rainfall_adj']),
                'label': crop
            })

# Create DataFrame
ml_ready_df = pd.DataFrame(expanded_data)

# Save to CSV
ml_ready_df.to_csv('data/tn_crop_recommendation_ml_ready.csv', index=False)

print(f"✅ Created ML-ready dataset with {len(ml_ready_df)} rows")
print(f"Districts: {ml_ready_df['District'].nunique()}")
print(f"Crops: {ml_ready_df['label'].nunique()}")
print(f"Seasons: {ml_ready_df['Season'].nunique()}")
print("\nFirst few rows:")
print(ml_ready_df.head())
print("\nCrop distribution:")
print(ml_ready_df['label'].value_counts())
