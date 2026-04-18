# Tamil Nadu Crop Recommendation System

An AI/ML capstone project focused on crop recommendation for the Thanjavur region of Tamil Nadu. The project combines soil survey data, weather records, historical crop price and yield information, and crop requirement tables to support crop suitability analysis and profitability comparison.

The current working application is a Streamlit dashboard in [app.py](app.py) that turns the prepared datasets into three practical views:

1. yield potential ranking
2. profitability ranking
3. a rule-based crop suitability predictor

## What This Project Is Trying To Solve

Farmers and planners usually need more than a single crop label. They want to know:

1. which crops perform well in the region,
2. which crops appear more profitable in the market,
3. and which crops match the current soil and climate conditions.

This project addresses those questions by bringing the data together in one place and presenting the results in an interactive dashboard.

## End-To-End Project Flow

The project is organized as a step-by-step pipeline. The README below follows the same order the data moves through the system.

### Step 1: Collect and Organize the Raw Data

The repository keeps multiple data sources under the [Data](Data) folder.

Important inputs used by the dashboard are:

1. [Data/Soil Data ( District Wise)/CSV Format/THANJAVUR.csv](Data/Soil%20Data%20(%20District%20Wise)/CSV%20Format/THANJAVUR.csv)
2. [Data/Weather Data (District Wise)/weather_data_all_blocks.csv](Data/Weather%20Data%20(District%20Wise)/weather_data_all_blocks.csv)
3. [Data/3_Cleaned CSVs/](Data/3_Cleaned%20CSVs)
4. [Data/Crop Area And Yield Data.csv](Data/Crop%20Area%20And%20Yield%20Data.csv)
5. [Data/crop_requirements.csv](Data/crop_requirements.csv)

These files feed the analysis in the dashboard. If any of the filenames or folder paths change, the app will need to be updated accordingly.

### Step 2: Consolidate Fragmented Crop CSV Files

Some crop price files were originally split across multiple year ranges, such as separate files for different periods. The utility script [consolidate_crop_csvs.py](consolidate_crop_csvs.py) combines those fragments into one file per crop.

What this step does:

1. scans [Data/3_Cleaned CSVs](Data/3_Cleaned%20CSVs) for crop CSV files,
2. groups files that belong to the same crop,
3. merges split year-based files into a single consolidated CSV,
4. removes duplicate rows,
5. writes the cleaned result into [Data/3_Cleaned CSVs/Consolidated](Data/3_Cleaned%20CSVs/Consolidated),
6. and keeps the merged crop file ready for downstream analysis.

This is the data-preparation stage that makes the price dataset consistent across crops.

### Step 3: Replace Fragmented Files With Consolidated Versions

The script [replace_with_consolidated.py](replace_with_consolidated.py) is the cleanup step that copies the consolidated crop files back into the original crop data folder and removes the old fragmented files.

This ensures the dashboard loads one consistent file per crop instead of juggling multiple period-specific files.

### Step 4: Inspect the Regional Soil and Crop Data

The analysis script [thanjavur_region_analysis.py](thanjavur_region_analysis.py) is a region-focused inspection tool. It loads Thanjavur soil data and the crop price data, then prints summaries such as:

1. soil nutrient distribution,
2. pH distribution,
3. organic carbon status,
4. micronutrient availability,
5. salinity status,
6. crop price ranges,
7. crop record counts,
8. and date coverage where available.

This script is useful for understanding the region before building the recommendation logic.

### Step 5: Check the Local Python Environment

The helper script [check_cuda.py](check_cuda.py) verifies whether PyTorch can access CUDA on the machine.

This is not required for the Streamlit dashboard, but it is useful when testing notebook-based machine learning experiments that may use deep learning models.

### Step 6: Load and Normalize Data in the Dashboard

The Streamlit application in [app.py](app.py) performs the main runtime processing.

At startup it does the following:

1. loads the Thanjavur soil CSV,
2. loads the district weather dataset and filters it to Thanjavur,
3. loads all crop CSVs from [Data/3_Cleaned CSVs](Data/3_Cleaned%20CSVs),
4. loads crop requirement data from [Data/crop_requirements.csv](Data/crop_requirements.csv),
5. loads crop area and yield data from [Data/Crop Area And Yield Data.csv](Data/Crop%20Area%20And%20Yield%20Data.csv),
6. normalizes crop names so that similar names match even when punctuation differs,
7. converts area and yield values to numeric form,
8. and aggregates crop area and yield statistics using medians.

This normalization step is important because different files may spell the same crop name slightly differently.

### Step 7: Build Yield Rankings

The dashboard creates a yield-oriented ranking from historical area and yield data.

It calculates:

1. median cultivated area per crop,
2. median yield per crop,
3. a normalized yield potential score,
4. a normalized area potential score,
5. and a combined score that gives more weight to yield than area.

The result is a list of crops that have strong historical production potential in the region.

### Step 8: Build Profitability Rankings

The dashboard also estimates a profit proxy from the market price data.

For each crop it computes:

1. average modal price,
2. median modal price,
3. price variation,
4. the number of available price records,
5. an approximate gross revenue proxy using price multiplied by median yield,
6. and a normalized profit score.

This gives a market-oriented view of which crops appear more attractive financially.

### Step 9: Score Crop Suitability From User Inputs

The prediction tab in [app.py](app.py) is not a black-box ML classifier. It is a transparent rule-based scoring system built on the crop requirement table.

The user can adjust:

1. nitrogen level,
2. phosphorus level,
3. potassium level,
4. soil pH category,
5. organic carbon level,
6. temperature range,
7. rainfall range,
8. humidity preference,
9. and season.

The script compares those selections with the crop requirement record and then penalizes mismatches. Crops that better match the selected conditions receive higher scores.

This makes the recommendation logic easy to explain during a presentation.

### Step 10: Present the Results in a Streamlit UI

The dashboard is split into four tabs:

1. Recommendations
2. Yield Analysis
3. Profit Analysis
4. Prediction Tool

Each tab is described in detail below.

## Dashboard Walkthrough

### Tab 1: Recommendations

This is the overview screen.

It shows:

1. the top crops by yield potential,
2. the top crops by profitability,
3. a bar chart for the top 10 yield crops,
4. and a bar chart for the top 10 profitable crops.

Use this tab when you want to present the headline outcome quickly.

### Tab 2: Yield Analysis

This tab is for deeper inspection of the production side.

It includes:

1. total crops analyzed,
2. average median yield,
3. maximum yield score,
4. a search box for crop names,
5. a minimum score slider,
6. a sortable data table,
7. and a scatter plot showing area versus yield.

The bubble size and color show the combined ranking score, which helps you see which crops are strong both in area and in yield.

### Tab 3: Profit Analysis

This tab focuses on the market side of the project.

It includes:

1. the number of crops analyzed for profitability,
2. average market price,
3. the maximum profit score,
4. crop name search,
5. a minimum average price filter,
6. a table of price and revenue metrics,
7. a scatter plot of price versus yield,
8. and a bar chart of the top revenue-proxy crops.

Use this tab to explain that crop choice is not only about agronomy, but also about market return.

### Tab 4: Prediction Tool

This is the interactive suitability checker.

It allows the user to simulate soil and climate conditions and then rank crops based on the crop requirement table.

The output has two parts:

1. a ranked table of the most suitable crops,
2. and a bar chart of the top suitability scores.

This tab is useful for demoing how a practical recommendation changes as input conditions change.

## Repository Structure

The most relevant files and folders are:

1. [app.py](app.py) - main Streamlit dashboard
2. [consolidate_crop_csvs.py](consolidate_crop_csvs.py) - merges split crop CSV files
3. [replace_with_consolidated.py](replace_with_consolidated.py) - swaps fragmented files for consolidated files
4. [thanjavur_region_analysis.py](thanjavur_region_analysis.py) - regional data analysis script
5. [check_cuda.py](check_cuda.py) - optional CUDA/PyTorch environment check
6. [requirements.txt](requirements.txt) - Python dependencies
7. [DEMO_INSTRUCTIONS.md](DEMO_INSTRUCTIONS.md) - short demo runbook
8. [Data/](Data) - soil, weather, crop, area, yield, and requirement datasets
9. [Models/](Models) - saved model artifacts and analysis outputs
10. notebook files such as [Crop_Recommendation_AI_ML.ipynb](Crop_Recommendation_AI_ML.ipynb) and [Crop_Recommendation_System.ipynb](Crop_Recommendation_System.ipynb) - experimentation and development notebooks

## How To Run The Project

### 1. Create or activate the virtual environment

The repository already uses a local virtual environment in [.venv](.venv) on the current machine.

If you need to activate it manually in PowerShell:

```powershell
& "c:\Users\tanis\Documents\Project 2\Project---2\.venv\Scripts\Activate.ps1"
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch the dashboard

```bash
streamlit run app.py
```

The app opens in the browser at `http://localhost:8501`.

## Detailed Working Logic

This section summarizes the actual processing order used by the dashboard.

### Data loading

The dashboard loads data once and caches it so the page stays fast after the first run.

### Data cleaning

Crop names are normalized by removing spaces and punctuation so that related files can be matched reliably.

### Aggregation

Area and yield records are converted into median values because medians are more stable than raw averages when the data contains outliers.

### Ranking

Yield ranking and profitability ranking are computed separately so that agronomic performance and market performance can be compared side by side.

### Suitability scoring

The predictor uses a simple additive penalty system. When a crop requirement is not matched, the score decreases. This keeps the output interpretable for users during a demo.

## Why This Project Is Useful

1. It is region-specific rather than generic.
2. It uses multiple data sources instead of a single dataset.
3. It combines production potential and market value.
4. It provides an explainable demo instead of a hidden scoring system.
5. It is practical for a presentation because the results are easy to inspect visually.

## Current Limitations

1. The dashboard is focused on Thanjavur and is not yet generalized to every district in Tamil Nadu.
2. The suitability tool is rule-based rather than a full trained classifier.
3. The app depends on the current folder structure and file names.
4. The notebooks and model artifacts are exploratory and may not all be wired into the Streamlit app.

## Future Improvements

1. Turn the district-specific dashboard into a multi-district recommender.
2. Replace the rule-based predictor with a trained model if a validated dataset is available.
3. Add download buttons for CSV or PDF reports.
4. Add a map-based district selector.
5. Connect live weather APIs for current-season recommendations.
6. Add richer explainability charts for the ranking outputs.

## Troubleshooting

### Streamlit cannot find a module

Reinstall the dependencies:

```bash
pip install --upgrade streamlit pandas numpy matplotlib seaborn scikit-learn
```

### The app says the data path is missing

Check that the repository is still located at the expected path and that the [Data](Data) folder exists with the same filenames.

### The dashboard is slow the first time

The first load reads several CSV files and builds the rankings. Later reloads are faster because the data-loading functions are cached.

## Project Summary

This project is a complete crop analysis workflow for Thanjavur:

1. prepare and consolidate crop data,
2. inspect regional soil and price patterns,
3. aggregate yield and market information,
4. compute yield and profitability rankings,
5. score crop suitability from soil and climate inputs,
6. and present everything in a Streamlit dashboard.

That structure makes the project suitable both as an academic capstone and as a demo for practical agricultural decision support.
