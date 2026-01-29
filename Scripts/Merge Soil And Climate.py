import pandas as pd
import os
import numpy as np

# Set project root
project_root = r'C:\Users\acer\PycharmProjects\Project---2'

# Load data
soil_path = os.path.join(project_root, 'data', 'average_soil_nutrients_tn_districtwise.csv')
climate_path = os.path.join(project_root, 'data', 'tn_climate_10years_seasonal.csv')

soil_df = pd.read_csv(soil_path)
climate_df = pd.read_csv(climate_path)


def calculate_crop_suitability_score(district, season, temp, rainfall, ph, crop, district_crops):
    """
    Calculate suitability score (0-100) for each crop based on conditions.
    Higher score = better match. Allows multiple crops per condition.
    """
    if crop not in district_crops:
        return 0  # Crop can't be grown in this district

    score = 50  # Base score

    # === RICE SCORING ===
    if crop == 'rice':
        # Rainfall preference
        if rainfall > 150:
            score += 30
        elif rainfall > 100:
            score += 20
        elif rainfall > 75:
            score += 10
        else:
            score -= 20

        # Season preference
        if season in ['Kharif', 'Rabi']:
            score += 15
        # pH preference
        if 6.0 <= ph <= 7.0:
            score += 10
        elif 5.5 <= ph <= 7.5:
            score += 5
        # Temperature
        if 22 <= temp <= 32:
            score += 10
    # === COTTON SCORING ===
    elif crop == 'cotton':
        # Rainfall (moderate preference)
        if 50 <= rainfall <= 100:
            score += 25
        elif 100 <= rainfall <= 150:
            score += 15
        else:
            score -= 10

        # Season
        if season in ['Kharif', 'Summer']:
            score += 15

        # Temperature
        if 21 <= temp <= 30:
            score += 15

        # pH
        if 6.5 <= ph <= 8.0:
            score += 10

    # === GROUNDNUT SCORING ===
    elif crop == 'groundnut':
        # Rainfall (moderate)
        if 50 <= rainfall <= 125:
            score += 25
        elif 125 <= rainfall <= 150:
            score += 10
        else:
            score -= 15

        # Season
        if season in ['Kharif', 'Summer']:
            score += 15

        # Temperature
        if 20 <= temp <= 30:
            score += 15

        # pH
        if 5.3 <= ph <= 6.6:
            score += 10

    # === SUGARCANE SCORING ===
    elif crop == 'sugarcane':
        # High rainfall preference
        if rainfall > 200:
            score += 30
        elif rainfall > 150:
            score += 20
        else:
            score -= 20

        # Temperature
        if temp > 21:
            score += 15

        # pH
        if 6.5 <= ph <= 7.5:
            score += 10

    # === MILLETS SCORING ===
    elif crop == 'millets':
        # Low rainfall tolerance
        if rainfall < 75:
            score += 30
        elif rainfall < 100:
            score += 20
        else:
            score -= 10

        # Season
        if season in ['Kharif', 'Rabi']:
            score += 15

        # Temperature (heat tolerant)
        if 25 <= temp <= 35:
            score += 15

        # pH
        if ph > 5.5:
            score += 10

    # === PULSES SCORING ===
    elif crop == 'pulses':
        # Moderate rainfall
        if 40 <= rainfall <= 80:
            score += 25
        elif 80 <= rainfall <= 100:
            score += 15
        # Season
        if season in ['Rabi', 'Summer']:
            score += 15

        # Temperature
        if 15 <= temp <= 30:
            score += 15

        # pH
        if 6.0 <= ph <= 7.5:
            score += 10

    # === TURMERIC SCORING ===
    elif crop == 'turmeric':
        # High rainfall
        if rainfall > 150:
            score += 30
        elif rainfall > 100:
            score += 15
        # Season
        if season == 'Kharif':
            score += 20

        # Temperature
        if 20 <= temp <= 30:
            score += 15

        # pH
        if 5.5 <= ph <= 7.5:
            score += 10

    # === BANANA SCORING ===
    elif crop == 'banana':
        # Moderate-high rainfall
        if rainfall > 100:
            score += 25
        elif rainfall > 75:
            score += 15
        # Temperature
        if temp > 15:
            score += 15

        # pH
        if 6.0 <= ph <= 7.5:
            score += 10

    # === COCONUT SCORING ===
    elif crop == 'coconut':
        # Very high rainfall
        if rainfall > 200:
            score += 35
        else:
            score -= 25

        # Coastal districts only
        if district in ['Kanyakumari', 'Tiruppur', 'Cuddalore', 'Villupuram']:
            score += 20

        # Temperature
        if temp > 20:
            score += 10
    # === TEA SCORING ===
    elif crop == 'tea':
        # High altitude (Nilgiris only)
        if district == 'The Nilgiris':
            score += 40
        else:
            return 0  # Can't grow tea outside Nilgiris

        # High rainfall
        if rainfall > 150:
            score += 20

        # Cool temperature
        if temp < 25:
            score += 15

    # === COFFEE SCORING ===
    elif crop == 'coffee':
        # Similar to tea
        if district == 'The Nilgiris':
            score += 40
        else:
            return 0

        if rainfall > 150:
            score += 20

        if 15 <= temp <= 28:
            score += 15

    # === VEGETABLES SCORING ===
    elif crop == 'vegetables':
        # Flexible conditions
        if 10 <= temp <= 30:
            score += 15
        if rainfall > 50:
            score += 15

        # Available year-round
        score += 10

    # === MAIZE SCORING ===
    elif crop == 'maize':
        # Moderate rainfall
        if 50 <= rainfall <= 100:
            score += 25

        # Season
        if season in ['Kharif', 'Rabi']:
            score += 15

        # Temperature
        if 21 <= temp <= 27:
            score += 15

        # pH
        if 5.5 <= ph <= 7.0:
            score += 10

    # === OTHER CROPS (GENERIC) ===
    else:
        # Generic scoring for remaining crops
        if 20 <= temp <= 30:
            score += 10
        if 75 <= rainfall <= 150:
            score += 10
        if 6.0 <= ph <= 7.5:
            score += 10
    return max(0, min(100, score))  # Clamp to 0-100


# District crop possibilities
district_crop_options = {
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

# Generate dataset with probabilistic assignment
final_data = []

for _, climate_row in climate_df.iterrows():
    district = climate_row['District']
    soil_row = soil_df[soil_df['District'] == district].iloc[0]

    district_crops = district_crop_options.get(district, ['rice'])

    # Calculate suitability for all crops
    crop_scores = {}
    for crop in district_crops:
        score = calculate_crop_suitability_score(
            district=district,
            season=climate_row['Season'],
            temp=climate_row['temperature'],
            rainfall=climate_row['rainfall'],
            ph=soil_row['pH'],
            crop=crop,
            district_crops=district_crops
        )
        crop_scores[crop] = score

    # Select crops with score >= 50 (suitable threshold)
    suitable_crops = [crop for crop, score in crop_scores.items() if score >= 50]

    # If no crops meet threshold, take top 1-2 crops
    if not suitable_crops:
        sorted_crops = sorted(crop_scores.items(), key=lambda x: x[1], reverse=True)
        suitable_crops = [crop for crop, _ in sorted_crops[:2]]

    # Create entries for suitable crops
    for crop in suitable_crops:
        final_data.append({
            'District': district,
            'year': int(climate_row['year']),
            'Season': climate_row['Season'],
            'N': soil_row['N_Kg_Ha'],
            'P': soil_row['P_Kg_Ha'],
            'K': soil_row['K_Kg_Ha'],
            'pH': soil_row['pH'],
            'EC': soil_row['EC_dS_m'],
            'OC': soil_row['OC_percent'],
            'S': soil_row['S_ppm'],
            'B': soil_row['B_ppm'],
            'Zn': soil_row['Zn_ppm'],
            'Cu': soil_row['Cu_ppm'],
            'Fe': soil_row['Fe_ppm'],
            'Mn': soil_row['Mn_ppm'],
            'temperature': climate_row['temperature'],
            'temperature_max': climate_row['temperature_max'],
            'temperature_min': climate_row['temperature_min'],
            'humidity': climate_row['humidity'],
            'rainfall': climate_row['rainfall'],
            'label': crop,
            'suitability_score': crop_scores[crop]  # Added for reference
        })

final_df = pd.DataFrame(final_data)

# Save
output_path = os.path.join(project_root, 'data', 'tn_crop_recommendation_scored.csv')
final_df.to_csv(output_path, index=False)

print(f"✅ Score-based dataset created!")
print(f"Saved to: {output_path}")
print(f"Total rows: {len(final_df)}")
print(f"\nCrop distribution:\n{final_df['label'].value_counts()}")
print(f"\nAverage suitability score: {final_df['suitability_score'].mean():.1f}")
print(f"\nSamples per season:")
print(final_df.groupby('Season')['label'].count())
