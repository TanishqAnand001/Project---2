# Smart Agriculture Data Pipeline and Regional Analytics

This project builds a district-level agriculture intelligence pipeline for Tamil Nadu by combining:

- Soil health data (district and block level)
- Crop market price and yield datasets
- Weather summaries derived from Open-Meteo historical APIs

The repository contains data cleaning utilities, consolidation scripts, weather data extraction, and a detailed regional analysis workflow (currently focused on Thanjavur district).

## What this project does

1. Converts raw Excel soil datasets to CSV format.
2. Merges fragmented crop CSV files into consolidated crop-level files.
3. Replaces split crop files with clean consolidated versions.
4. Extracts and summarizes weather signals for each district block.
5. Performs district-level analytics (soil + crop price insights) and generates visual reports.

## Tech stack

- Python 3.10+
- pandas, numpy
- matplotlib, seaborn
- scikit-learn (available for downstream modeling)
- streamlit (available for dashboard/app extensions)
- requests (used in weather collection script)

Dependencies are listed in `requirements.txt`.

## Repository structure

```text
Project---2/
|-- Data/
|   |-- 3_Cleaned CSVs/
|   |   |-- Consolidated/
|   |-- Crop Area And Yield Data.csv
|   |-- crop_requirements.csv
|   |-- Crop Data/
|   |-- Soil Data ( District Wise)/
|   |   |-- CSV Format/
|   |   |-- Excel Format/
|   |-- Weather Data (District Wise)/
|       |-- weather_data_all_blocks.csv
|       |-- Raw Daily/
|-- Scripts/
|   |-- Excel To CSV.py
|   |-- Combine CSV.py
|   |-- ReplaceWithConsolidated.py
|   |-- Weather Data Collection.py
|   |-- Region Analysis.py
|-- Models/
|-- requirements.txt
|-- Untitled-2.ipynb
```

## Data folders explained

- `Data/Soil Data ( District Wise)/Excel Format/`
  - Original Excel sources for soil metrics.
- `Data/Soil Data ( District Wise)/CSV Format/`
  - District-wise soil CSV files used by analysis and weather scripts.
- `Data/3_Cleaned CSVs/`
  - Crop market/price data after cleaning.
  - Contains both split files (with year suffixes) and single crop files.
- `Data/3_Cleaned CSVs/Consolidated/`
  - Output from consolidation scripts.
- `Data/Weather Data (District Wise)/Raw Daily/`
  - Per-block daily weather time series files.
- `Data/Weather Data (District Wise)/weather_data_all_blocks.csv`
  - Final block-level summarized weather features.

## Scripts and workflow

### 1) Excel to CSV conversion
File: `Scripts/Excel To CSV.py`

Purpose:
- Converts one or many `.xlsx` files to `.csv`.
- Handles multi-sheet workbooks by exporting one CSV per sheet.

Modes:
- Single Excel file
- Folder batch conversion
- Project data-target mode (preconfigured option in script)

Typical run:

```powershell
python "Scripts/Excel To CSV.py"
```

### 2) Consolidate split crop files
File: `Scripts/Combine CSV.py`

Purpose:
- Detects crop files split by year ranges (for example, `Paddy-2015-2019.csv`, `Paddy-2019-2022.csv`).
- Merges and deduplicates records.
- Writes consolidated outputs into `Data/3_Cleaned CSVs/Consolidated/`.

Typical run:

```powershell
python "Scripts/Combine CSV.py"
```

### 3) Replace fragmented files with consolidated versions
File: `Scripts/ReplaceWithConsolidated.py`

Purpose:
- Copies consolidated files back into `Data/3_Cleaned CSVs/`.
- Deletes old fragmented files with year-suffix naming patterns.

Typical run:

```powershell
python "Scripts/ReplaceWithConsolidated.py"
```

### 4) Weather data extraction and aggregation
File: `Scripts/Weather Data Collection.py`

Purpose:
- Reads unique `(District, Block)` combinations from soil CSV files.
- Geocodes blocks with Nominatim (OpenStreetMap).
- Calls Open-Meteo historical APIs to fetch daily weather and hourly soil variables.
- Computes summarized agro-climate indicators.
- Saves:
  - Raw daily files per block in `Data/Weather Data (District Wise)/Raw Daily/`
  - Consolidated summary in `Data/Weather Data (District Wise)/weather_data_all_blocks.csv`

Notes:
- The script includes intentional waiting between API calls to reduce rate-limit risk.
- Internet access is required.

Typical run:

```powershell
python "Scripts/Weather Data Collection.py"
```

### 5) Regional analysis (Thanjavur focus)
File: `Scripts/Region Analysis.py`

Purpose:
- Loads Thanjavur soil profile from district soil data.
- Filters crop price files for Thanjavur records.
- Computes nutrient, pH, micronutrient, and crop-price insights.
- Generates visualization PNGs in the project root:
  - `soil_macronutrients.png`
  - `soil_pH_distribution.png`
  - `soil_micronutrients.png`
  - `soil_block_comparison.png`
  - `crop_prices_comparison.png`
  - `crop_records_count.png`

Typical run:

```powershell
python "Scripts/Region Analysis.py"
```

## Setup instructions

### 1) Create and activate virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
pip install -r requirements.txt
pip install requests
```

`requests` is used by weather collection and may need to be added to `requirements.txt` if missing.

## Recommended execution order

1. Convert Excel files to CSV (if new Excel data is added).
2. Consolidate split crop files.
3. Replace fragmented files with consolidated files.
4. Collect weather data and generate weather summary table.
5. Run district analysis to produce insights and plots.

## Current outputs

- Consolidated crop CSV files under `Data/3_Cleaned CSVs/Consolidated/`
- Cleaned crop CSV set in `Data/3_Cleaned CSVs/`
- Weather summary table: `Data/Weather Data (District Wise)/weather_data_all_blocks.csv`
- Per-block weather histories: `Data/Weather Data (District Wise)/Raw Daily/`
- Thanjavur analysis plots in project root

## Known limitations

- Some scripts use absolute Windows paths; portability may be limited across machines.
- Current regional analytics are centered on Thanjavur and can be generalized for other districts.
- `Models/` is currently empty (model training pipeline can be added next).
- `Untitled-2.ipynb` exists for experimentation but is not yet documented as a production workflow.

## Suggested next improvements

- Add CLI arguments to all scripts (`argparse`) to avoid hard-coded paths.
- Add logging and validation checks for missing columns/files.
- Add model training and evaluation scripts inside `Models/`.
- Add a Streamlit dashboard to visualize district trends interactively.
- Add tests for data transformation utilities.

## License

No explicit license file is currently present. Add a `LICENSE` file if this project will be shared publicly.

## Author notes

This repository already has a strong data engineering base for an agriculture intelligence platform. The next milestone can be a full prediction workflow (for yield, price, or crop suitability) using the prepared soil-weather-market feature sets.
