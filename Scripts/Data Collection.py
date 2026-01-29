"""
Tamil Nadu Crop Recommendation Dataset Collection - FIXED VERSION
=================================================================
This script helps collect soil and climate data for Tamil Nadu crop prediction project.

FIXED: NASA POWER API now requests ONE parameter at a time (API limitation)

Data Sources:
1. Kaggle - Crop Recommendation Dataset (baseline)
2. NASA POWER - Climate data for Tamil Nadu
3. Ready-to-use datasets from Kaggle
"""

import requests
import pandas as pd
import json
from datetime import datetime
import time
import os

# ============================================================================
# PART 1: Download NASA POWER Climate Data for Tamil Nadu - FIXED
# ============================================================================

def download_nasa_power_data(start_year=2019, end_year=2024):
    """
    Download climate data for Tamil Nadu from NASA POWER API
    Tamil Nadu coordinates: Lat: 8°N to 13.5°N, Long: 76.5°E to 80.5°E

    FIXED: Downloads one parameter at a time due to API limitation
    """
    print("=" * 60)
    print("DOWNLOADING NASA POWER CLIMATE DATA FOR TAMIL NADU")
    print("=" * 60)

    # Tamil Nadu central point (using point data instead of regional for reliability)
    # Central TN coordinates (approximately Chennai/Madurai area)
    lat = 11.0
    lon = 78.5

    # Base URL for NASA POWER API - using point data
    base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    # Parameters we need for crop recommendation
    # We'll download each parameter separately
    parameters_list = [
        ("T2M", "Temperature at 2m (°C)"),
        ("T2M_MAX", "Maximum Temperature (°C)"),
        ("T2M_MIN", "Minimum Temperature (°C)"),
        ("RH2M", "Relative Humidity at 2m (%)"),
        ("PRECTOTCORR", "Precipitation (mm/day)")
    ]

    # Create directory for climate data
    os.makedirs("data/climate_data", exist_ok=True)

    all_data = {}

    for year in range(start_year, end_year + 1):
        print(f"\n{'='*60}")
        print(f"Downloading data for year {year}...")
        print(f"{'='*60}")

        year_data = {}

        # Download each parameter separately
        for param_code, param_name in parameters_list:
            print(f"\n  Fetching {param_name}...", end=" ")

            params = {
                "parameters": param_code,  # ONE parameter at a time
                "community": "AG",
                "format": "JSON",
                "latitude": lat,
                "longitude": lon,
                "start": f"{year}0101",
                "end": f"{year}1231"
            }

            try:
                response = requests.get(base_url, params=params, timeout=120)
                response.raise_for_status()

                data = response.json()

                # Extract the parameter data
                if 'properties' in data and 'parameter' in data['properties']:
                    year_data[param_code] = data['properties']['parameter'][param_code]
                    print("✓")
                else:
                    print("✗ (No data in response)")

                # Be nice to the API - wait between requests
                time.sleep(2)

            except requests.exceptions.RequestException as e:
                print(f"✗ Error: {e}")
                continue
            except Exception as e:
                print(f"✗ Parse error: {e}")
                continue

        # Save combined data for this year
        if year_data:
            all_data[year] = year_data

            # Save to file
            output_file = f"data/climate_data/tn_climate_{year}.json"
            with open(output_file, "w") as f:
                json.dump(year_data, f, indent=2)

            print(f"\n  ✓ Saved: {output_file}")

            # Convert to CSV for easier viewing
            df = convert_to_dataframe(year_data, year)
            csv_file = f"data/climate_data/tn_climate_{year}.csv"
            df.to_csv(csv_file, index=False)
            print(f"  ✓ Saved: {csv_file}")
        else:
            print(f"\n  ✗ No data collected for {year}")

    print("\n" + "=" * 60)
    print("NASA POWER data download complete!")
    print(f"Files saved in: data/climate_data/")
    print("=" * 60)

    return all_data

def convert_to_dataframe(year_data, year):
    """
    Convert the NASA POWER JSON data to a pandas DataFrame
    """
    # Get all dates from the first parameter
    dates = list(list(year_data.values())[0].keys())

    records = []
    for date in dates:
        record = {'date': date, 'year': year}

        # Add all parameters
        for param_code, values in year_data.items():
            record[param_code] = values.get(date, None)

        records.append(record)

    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

    # Rename columns for clarity
    column_mapping = {
        'T2M': 'temperature',
        'T2M_MAX': 'temp_max',
        'T2M_MIN': 'temp_min',
        'RH2M': 'humidity',
        'PRECTOTCORR': 'rainfall'
    }
    df = df.rename(columns=column_mapping)

    return df

def create_monthly_summary():
    """
    Create monthly summaries from the downloaded daily data
    """
    print("\n" + "=" * 60)
    print("CREATING MONTHLY SUMMARIES")
    print("=" * 60)

    climate_dir = "data/climate_data"

    if not os.path.exists(climate_dir):
        print("✗ No climate data found. Please download data first.")
        return

    # Read all CSV files
    all_dfs = []
    for filename in os.listdir(climate_dir):
        if filename.endswith('.csv'):
            filepath = os.path.join(climate_dir, filename)
            df = pd.read_csv(filepath)
            df['date'] = pd.to_datetime(df['date'])
            all_dfs.append(df)

    if not all_dfs:
        print("✗ No CSV files found")
        return

    # Combine all years
    combined_df = pd.concat(all_dfs, ignore_index=True)

    # Create monthly aggregates
    combined_df['year'] = combined_df['date'].dt.year
    combined_df['month'] = combined_df['date'].dt.month

    monthly_df = combined_df.groupby(['year', 'month']).agg({
        'temperature': 'mean',
        'temp_max': 'mean',
        'temp_min': 'mean',
        'humidity': 'mean',
        'rainfall': 'sum'  # Sum for monthly rainfall
    }).reset_index()

    # Round to 2 decimal places
    monthly_df = monthly_df.round(2)

    # Save monthly summary
    output_file = "data/climate_data/tn_climate_monthly_summary.csv"
    monthly_df.to_csv(output_file, index=False)

    print(f"\n✓ Monthly summary created: {output_file}")
    print(f"Total months: {len(monthly_df)}")
    print("\nSample data:")
    print(monthly_df.head(10))
    print("\n" + "=" * 60)

    return monthly_df

# ============================================================================
# PART 2: Download Kaggle Crop Recommendation Dataset
# ============================================================================

def download_kaggle_datasets():
    """
    Instructions for downloading Kaggle datasets
    """
    print("\n" + "=" * 60)
    print("KAGGLE DATASETS - MANUAL DOWNLOAD REQUIRED")
    print("=" * 60)

    datasets = {
        "1. Crop Recommendation Dataset": {
            "url": "https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset",
            "description": "Contains NPK, pH, rainfall, temperature, humidity for 22 crops",
            "command": "kaggle datasets download -d atharvaingle/crop-recommendation-dataset"
        },
        "2. Tamil Nadu Crop Production": {
            "url": "https://www.kaggle.com/datasets/aishu200023/tamilnadu-cropproduction",
            "description": "District-wise crop production data for Tamil Nadu",
            "command": "kaggle datasets download -d aishu200023/tamilnadu-cropproduction"
        },
        "3. India Agriculture Dataset": {
            "url": "https://www.kaggle.com/datasets/thammuio/all-agriculture-related-datasets-for-india",
            "description": "Comprehensive agriculture data for India",
            "command": "kaggle datasets download -d thammuio/all-agriculture-related-datasets-for-india"
        }
    }

    print("\nTo download these datasets, you need a Kaggle account and API key.\n")
    print("SETUP STEPS:")
    print("1. Create account at https://www.kaggle.com")
    print("2. Go to Account Settings > API > Create New Token")
    print("3. This downloads kaggle.json - place it in ~/.kaggle/")
    print("4. Install kaggle: pip install kaggle")
    print("5. Run the commands below:\n")

    for name, info in datasets.items():
        print(f"\n{name}")
        print("-" * 50)
        print(f"URL: {info['url']}")
        print(f"Description: {info['description']}")
        print(f"Command: {info['command']}")

    print("\n" + "=" * 60)

# ============================================================================
# PART 3: Create Sample Dataset Structure
# ============================================================================

def create_sample_dataset():
    """
    Create a sample CSV structure showing what your final dataset should look like
    """
    print("\n" + "=" * 60)
    print("CREATING SAMPLE DATASET STRUCTURE")
    print("=" * 60)

    # Sample data for Tamil Nadu crops
    sample_data = {
        'district': ['Coimbatore', 'Salem', 'Madurai', 'Thanjavur', 'Tirupur'] * 4,
        'N': [90, 85, 80, 100, 75, 88, 92, 78, 95, 82, 85, 90, 77, 98, 84, 91, 87, 79, 93, 81],
        'P': [42, 40, 38, 45, 35, 43, 41, 37, 44, 36, 40, 42, 35, 45, 38, 43, 41, 36, 44, 37],
        'K': [43, 45, 42, 50, 40, 44, 46, 41, 48, 39, 45, 43, 40, 50, 42, 46, 44, 41, 49, 40],
        'temperature': [28.5, 29.2, 31.0, 27.8, 28.9, 27.5, 28.8, 30.5, 27.2, 29.1,
                       28.3, 29.0, 30.8, 27.5, 28.7, 28.1, 29.3, 31.2, 27.6, 29.0],
        'humidity': [65, 68, 62, 70, 64, 66, 67, 63, 71, 65, 68, 66, 62, 70, 64, 67, 68, 63, 71, 65],
        'ph': [6.5, 6.8, 7.0, 6.2, 6.7, 6.6, 6.9, 7.1, 6.3, 6.8, 6.5, 6.7, 7.0, 6.2, 6.9, 6.6, 6.8, 7.1, 6.3, 6.7],
        'rainfall': [850, 920, 780, 1050, 800, 870, 950, 760, 1080, 820,
                     880, 930, 770, 1060, 810, 890, 940, 750, 1090, 830],
        'crop': ['Rice', 'Cotton', 'Sugarcane', 'Rice', 'Cotton',
                'Groundnut', 'Rice', 'Millets', 'Rice', 'Cotton',
                'Sugarcane', 'Rice', 'Millets', 'Rice', 'Cotton',
                'Groundnut', 'Rice', 'Sugarcane', 'Rice', 'Cotton']
    }

    df = pd.DataFrame(sample_data)

    # Create data directory
    os.makedirs("../data", exist_ok=True)

    # Save sample dataset
    df.to_csv("data/sample_tn_crop_dataset.csv", index=False)

    print("\n✓ Sample dataset created: data/sample_tn_crop_dataset.csv")
    print("\nDataset Structure:")
    print(df.head(10))
    print("\nDataset Info:")
    print(df.info())
    print("\nCrop Distribution:")
    print(df['crop'].value_counts())

    print("\n" + "=" * 60)

# ============================================================================
# PART 4: Data Collection Checklist
# ============================================================================

def print_collection_checklist():
    """
    Print a comprehensive checklist for data collection
    """
    print("\n" + "=" * 60)
    print("TAMIL NADU CROP PREDICTION - DATA COLLECTION CHECKLIST")
    print("=" * 60)

    checklist = """
    
DATA YOU NEED:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ SOIL DATA:
  - Nitrogen (N) content (kg/ha)
  - Phosphorus (P) content (kg/ha)
  - Potassium (K) content (kg/ha)
  - pH level (0-14 scale)
  - Soil type/texture

□ CLIMATE DATA:
  - Temperature (°C) - Min, Max, Average
  - Rainfall (mm)
  - Humidity (%)
  - Season information

□ CROP DATA:
  - Major TN crops: Rice, Cotton, Sugarcane, Groundnut, Millets, 
    Maize, Pulses, Vegetables, Coconut, Banana

□ LOCATION DATA:
  - District names (38 districts in TN)
  - Agro-climatic zones (7 zones in TN)


DATA SOURCES SUMMARY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. NASA POWER (Climate Data)
   ✓ Free, API access
   ✓ Historical climate data from 1981
   ✓ Temperature, rainfall, humidity
   → Use the script above to download

2. Kaggle Datasets
   ✓ Crop Recommendation Dataset - Ready to use
   ✓ TN Crop Production Dataset
   → Requires Kaggle account

3. Government Sources (Manual Download)
   • data.gov.in - Search "Tamil Nadu agriculture soil"
   • TNAU Agritech Portal - agritech.tnau.ac.in
   • TN Agriculture Dept - tnagriculture.in


RECOMMENDED APPROACH:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: Start with Kaggle Crop Recommendation Dataset
        → This gives you a baseline with all parameters

STEP 2: Download NASA POWER climate data for Tamil Nadu
        → Provides accurate recent climate data

STEP 3: Get TN-specific crop production data from Kaggle
        → Adds regional context

STEP 4: Combine datasets and add TN-specific values
        → Create your final training dataset


NEXT STEPS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Run this script to download NASA POWER data
2. Set up Kaggle API and download datasets
3. Combine and clean the data
4. Build your ML model
5. Validate predictions against known crop patterns

    """

    print(checklist)
    print("=" * 60)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function to orchestrate data collection
    """
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   TAMIL NADU CROP RECOMMENDATION - DATA COLLECTOR          ║")
    print("║   ** FIXED VERSION - ONE PARAMETER AT A TIME **            ║")
    print("╚════════════════════════════════════════════════════════════╝")

    print("\nWhat would you like to do?\n")
    print("1. Download NASA POWER climate data (Automated)")
    print("2. Create monthly summary from downloaded data")
    print("3. View Kaggle download instructions")
    print("4. Create sample dataset structure")
    print("5. View complete data collection checklist")
    print("6. Run everything")
    print("0. Exit")

    choice = input("\nEnter your choice (0-6): ").strip()

    if choice == "1":
        download_nasa_power_data()
    elif choice == "2":
        create_monthly_summary()
    elif choice == "3":
        download_kaggle_datasets()
    elif choice == "4":
        create_sample_dataset()
    elif choice == "5":
        print_collection_checklist()
    elif choice == "6":
        create_sample_dataset()
        download_nasa_power_data()
        create_monthly_summary()
        download_kaggle_datasets()
        print_collection_checklist()
    elif choice == "0":
        print("\nGoodbye!")
        return
    else:
        print("\nInvalid choice. Please run again.")
        return

    print("\n✓ Operation completed successfully!")
    print("\nNeed help? Check the documentation or feel free to ask!")

if __name__ == "__main__":
    main()