"""
Tamil Nadu Crop Recommendation - Comprehensive Dataset Combiner
================================================================
Combines:
1. Crop_recommendation.csv (soil baseline)
2. Tamilnadu agriculture yield data.csv (district–crop reality)
3. tn_climate_2019–2024.csv (actual climate)
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

# =============================================================================
# BASE PATH CONFIGURATION (WINDOWS / PYCHARM)
# =============================================================================

PROJECT_ROOT = r"C:\Users\acer\PycharmProjects\Project---2"

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
KAGGLE_DATASET_PATH = os.path.join(DATA_DIR, "kaggle_datasets")
CLIMATE_DATA_PATH = os.path.join(DATA_DIR, "climate_data")
OUTPUT_DIR = os.path.join(DATA_DIR, "processed")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =============================================================================
# DISTRICT – CROP MAPPING
# =============================================================================

DISTRICT_CROP_MAPPING = {
    'ARIYALUR': ['Rice', 'Groundnut', 'Cotton', 'Maize', 'Sugarcane'],
    'COIMBATORE': ['Cotton', 'Maize', 'Coconut', 'Banana', 'Vegetables'],
    'CUDDALORE': ['Rice', 'Groundnut', 'Sugarcane', 'Cashewnut'],
    'DHARMAPURI': ['Rice', 'Groundnut', 'Maize', 'Millets'],
    'DINDIGUL': ['Cotton', 'Maize', 'Coconut', 'Banana', 'Vegetables'],
    'ERODE': ['Turmeric', 'Maize', 'Cotton', 'Coconut', 'Banana'],
    'KANCHEEPURAM': ['Rice', 'Groundnut', 'Sugarcane', 'Vegetables'],
    'KANYAKUMARI': ['Rice', 'Coconut', 'Banana', 'Rubber', 'Vegetables'],
    'KARUR': ['Cotton', 'Maize', 'Groundnut', 'Coconut'],
    'KRISHNAGIRI': ['Maize', 'Tomato', 'Vegetables', 'Millets'],
    'MADURAI': ['Cotton', 'Rice', 'Groundnut', 'Vegetables'],
    'NAGAPATTINAM': ['Rice', 'Groundnut', 'Coconut', 'Cashewnut'],
    'NAMAKKAL': ['Maize', 'Groundnut', 'Cotton', 'Vegetables'],
    'PERAMBALUR': ['Rice', 'Groundnut', 'Cotton', 'Maize'],
    'PUDUKKOTTAI': ['Rice', 'Groundnut', 'Cotton', 'Coconut'],
    'RAMANATHAPURAM': ['Rice', 'Groundnut', 'Cotton', 'Coconut'],
    'SALEM': ['Rice', 'Maize', 'Groundnut', 'Millets', 'Vegetables'],
    'SIVAGANGA': ['Rice', 'Groundnut', 'Cotton', 'Coconut'],
    'THANJAVUR': ['Rice', 'Sugarcane', 'Groundnut', 'Coconut'],
    'THENI': ['Cotton', 'Maize', 'Banana', 'Coconut', 'Vegetables'],
    'TIRUCHIRAPPALLI': ['Rice', 'Cotton', 'Groundnut', 'Sugarcane'],
    'TIRUNELVELI': ['Rice', 'Cotton', 'Coconut', 'Banana'],
    'TIRUPPUR': ['Cotton', 'Maize', 'Coconut', 'Vegetables'],
    'TIRUVANNAMALAI': ['Rice', 'Groundnut', 'Sugarcane', 'Millets'],
    'TUTICORIN': ['Rice', 'Cotton', 'Groundnut', 'Coconut'],
    'VELLORE': ['Rice', 'Groundnut', 'Sugarcane', 'Vegetables'],
    'VILLUPURAM': ['Rice', 'Groundnut', 'Sugarcane', 'Cashewnut'],
    'VIRUDHUNAGAR': ['Cotton', 'Groundnut', 'Coconut', 'Chilli']
}

AGRO_ZONES = {
    'North Eastern': ['KANCHEEPURAM', 'TIRUVANNAMALAI', 'VELLORE', 'VILLUPURAM'],
    'North Western': ['DHARMAPURI', 'KRISHNAGIRI', 'SALEM', 'NAMAKKAL'],
    'Western': ['COIMBATORE', 'ERODE', 'TIRUPPUR', 'KARUR'],
    'Cauvery Delta': ['THANJAVUR', 'NAGAPATTINAM', 'TIRUCHIRAPPALLI', 'ARIYALUR', 'PERAMBALUR'],
    'Southern': ['MADURAI', 'DINDIGUL', 'THENI', 'VIRUDHUNAGAR', 'SIVAGANGA'],
    'Coastal': ['CUDDALORE', 'RAMANATHAPURAM', 'TUTICORIN'],
    'High Rainfall': ['KANYAKUMARI', 'TIRUNELVELI']
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_zone_for_district(district):
    for zone, districts in AGRO_ZONES.items():
        if district.upper() in districts:
            return zone
    return "Southern"

def get_season_from_month(month):
    if month in [6, 7, 8, 9, 10]:
        return "Kharif"
    elif month in [11, 12, 1, 2, 3]:
        return "Rabi"
    return "Summer"

# =============================================================================
# DATA LOADERS
# =============================================================================

def load_soil_baseline():
    df = pd.read_csv(os.path.join(KAGGLE_DATASET_PATH, "Crop_recommendation.csv"))
    df["label"] = df["label"].str.title()
    return df

def load_tn_yield_data():
    df = pd.read_csv(
        os.path.join(KAGGLE_DATASET_PATH, "Tamilnadu agriculture yield data.csv")
    )
    df["Crop"] = df["Crop"].str.title()
    df["District_Name"] = df["District_Name"].str.title()
    return df

def load_climate_data():
    dfs = []
    for year in range(2019, 2025):
        path = os.path.join(CLIMATE_DATA_PATH, f"tn_climate_{year}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            df["date"] = pd.to_datetime(df["date"])
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def create_monthly_climate_summary(df):
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    monthly = df.groupby(["year", "month"]).agg({
        "temperature": "mean",
        "temp_max": "mean",
        "temp_min": "mean",
        "humidity": "mean",
        "rainfall": "sum"
    }).reset_index()

    monthly["season"] = monthly["month"].apply(get_season_from_month)
    return monthly.round(2)

# =============================================================================
# MAIN COMBINATION LOGIC
# =============================================================================

def combine_datasets():
    soil = load_soil_baseline()
    climate_daily = load_climate_data()
    climate_monthly = create_monthly_climate_summary(climate_daily)
    yield_df = load_tn_yield_data()

    records = []

    for _, c in climate_monthly.iterrows():
        year, month, season = int(c.year), int(c.month), c.season

        season_data = yield_df[
            (yield_df["Crop_Year"] == year) &
            (yield_df["Season"].str.contains(season, case=False, na=False))
        ]

        for district in season_data["District_Name"].unique():
            crops = season_data[season_data["District_Name"] == district]["Crop"].unique()

            for crop in crops:
                soil_crop = soil[soil["label"] == crop]
                if soil_crop.empty:
                    continue

                s = soil_crop.median()

                records.append({
                    "year": year,
                    "month": month,
                    "season": season,
                    "district": district,
                    "zone": get_zone_for_district(district),
                    "N": s.N,
                    "P": s.P,
                    "K": s.K,
                    "ph": s.ph,
                    "temperature": c.temperature,
                    "temp_max": c.temp_max,
                    "temp_min": c.temp_min,
                    "humidity": c.humidity,
                    "rainfall": c.rainfall,
                    "crop": crop
                })

    return pd.DataFrame(records), climate_monthly

# =============================================================================
# EXPORT
# =============================================================================

def export_data(df, climate_monthly):
    df.to_csv(
        os.path.join(OUTPUT_DIR, "tamil_nadu_crop_dataset_2019_2024.csv"),
        index=False
    )
    climate_monthly.to_csv(
        os.path.join(OUTPUT_DIR, "tn_climate_monthly_2019_2024.csv"),
        index=False
    )

# =============================================================================
# MAIN
# =============================================================================

def main():
    combined_df, climate_monthly = combine_datasets()
    export_data(combined_df, climate_monthly)

    print("\n✅ DATASET GENERATED SUCCESSFULLY")
    print(f"Records: {len(combined_df)}")
    print(f"Saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
