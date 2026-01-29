import pandas as pd

# Load current data
df = pd.read_csv('../data/tn_crop_recommendation_real_climate.csv')

# Complete crop mapping for all districts
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

# Load soil data (to add micronutrients)
soil_df = pd.read_csv('../data/average_soil_nutrients_tn_districtwise.csv')

# Create expanded dataset
expanded_data = []

for _, row in df.iterrows():
    district = row['District']
    season = row['Season']

    # Get soil data for micronutrients
    soil_row = soil_df[soil_df['District'] == district].iloc[0]

    # Get all crops for this district
    crops = crop_labels.get(district, ['rice'])

    for crop in crops:
        expanded_data.append({
            'District': district,
            'Season': season,
            'N': row['N'],
            'P': row['P'],
            'K': row['K'],
            'pH': row['pH'],
            'EC': soil_row['EC_dS_m'],
            'OC': soil_row['OC_percent'],
            'S': soil_row['S_ppm'],
            'B': soil_row['B_ppm'],
            'Zn': soil_row['Zn_ppm'],
            'Cu': soil_row['Cu_ppm'],
            'Fe': soil_row['Fe_ppm'],
            'Mn': soil_row['Mn_ppm'],
            'temperature': row['temperature'],
            'humidity': row['humidity'],
            'rainfall': row['rainfall'],
            'label': crop
        })

# Create final DataFrame
final_df = pd.DataFrame(expanded_data)

# Save to CSV
final_df.to_csv('data/tn_crop_recommendation_complete.csv', index=False)

print(f"✅ Complete dataset created!")
print(f"Total rows: {len(final_df)}")
print(f"Districts: {final_df['District'].nunique()}")
print(f"Crops: {final_df['label'].nunique()}")
print(f"Seasons: {final_df['Season'].nunique()}")
print("\nCrop distribution:")
print(final_df['label'].value_counts().sort_values(ascending=False))
print("\nSample data:")
print(final_df.head(10))
print("\nColumns:", final_df.columns.tolist())
