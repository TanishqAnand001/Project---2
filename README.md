# Thanjavur Crop Recommendation - Model-Centric README

This project is a machine learning system for ranking crops using agro-climatic suitability and market-aware signals, with a primary focus on Thanjavur district.

The main modeling workflow lives in `Main Model.ipynb`.

## Modeling goal

Build a binary classifier that predicts whether a crop transaction is high-performing (`1`) or lower-performing (`0`), then use model probabilities plus historical productivity and profit proxies to generate practical crop rankings.

## End-to-end ML flow

The notebook follows a production-style sequence:

1. Imports and setup
2. Data loading and preprocessing
3. Feature engineering
4. Stratified train/test split
5. Multi-model training with multiple feature sets
6. Holdout and cross-validation evaluation
7. Ensemble-based crop ranking and recommendation

## Data used by the models

The model combines four feature domains:

- Soil profile features
  - N/P/K status, pH, EC salinity, organic carbon indicators
- Weather summary features
  - temperature, rainfall, humidity, rainy days, wind
- Crop requirement features
  - N/P/K requirement levels plus rainfall and temperature requirements
- Historical productivity features
  - area median, yield median, yield-per-area

Primary source files:

- `Data/Soil Data ( District Wise)/CSV Format/THANJAVUR.csv`
- `Data/Weather Data (District Wise)/weather_data_all_blocks.csv`
- `Data/3_Cleaned CSVs/*.csv`
- `Data/crop_requirements.csv`
- `Data/Crop Area And Yield Data.csv`

## Target construction

This is not trained directly on a labeled success column from raw data. Instead, the notebook builds a target proxy:

- Revenue proxy per transaction = modal market price x historical crop yield
- High-performing class = top quartile (>= 75th percentile) of the proxy
- Lower-performing class = remaining transactions

Important design choice:

- Price is excluded from model input features to avoid leakage and overweighting of market price in suitability learning.

## Feature sets evaluated

The notebook trains each model family on three feature bundles:

- `soil_weather`
- `soil_weather_requirements`
- `soil_weather_req_area_yield`

The third feature set is the richest and generally performs best in saved outputs.

## Model families trained

Core models:

- RandomForestClassifier
- GradientBoostingClassifier
- LogisticRegression
- SVC (RBF, probability enabled)

Optional boosted models (trained when libraries are installed):

- CatBoostClassifier
- XGBClassifier
- LGBMClassifier

Graceful fallback behavior:

- If CatBoost/XGBoost/LightGBM is missing, the notebook skips that block without stopping the entire training flow.

## Training and validation strategy

- Train/test split: stratified random 80/20
- Class imbalance handling:
  - balanced class weights for eligible models
  - scale-pos-weight style balancing for boosting models
- Cross-validation:
  - 5-fold StratifiedKFold on training data
  - includes optional row cap for large datasets
- Metrics tracked per experiment:
  - Accuracy
  - F1
  - PR-AUC (primary ranking metric)
  - ROC-AUC

Model selection policy:

- Leaderboard sorted primarily by holdout PR-AUC, then F1, then Accuracy.

## Current observed model behavior

From the saved notebook outputs/plots:

- Top experiments cluster around PR-AUC of approximately 0.80 to 0.84.
- Best-performing runs are primarily from:
  - `soil_weather_req_area_yield` feature set
  - Tree/boosting families (RandomForest, XGBoost, GradientBoosting, CatBoost, LightGBM)
- LogisticRegression and SVM remain competitive but generally rank lower than boosted/tree ensembles.

## Ensemble and recommendation logic

After training, the notebook creates an ensemble from the best variant of each trained model family.

It then produces three separate rankings:

1. High-performance probability
   - ensemble probability using non-price model features
2. Yield potential rank
   - historical productivity score
3. Profit proxy rank
   - market opportunity from price x yield

This separation keeps agronomic suitability and market profitability interpretable as distinct objectives.

## Artifacts and outputs

- Notebook with full ML pipeline:
  - `Main Model.ipynb`
- CatBoost training artifacts:
  - `catboost_info/catboost_training.json`
  - `catboost_info/learn_error.tsv`
  - `catboost_info/time_left.tsv`

Generated during notebook execution:

- Experiment leaderboard tables
- Top-experiments PR-AUC bar charts
- Classification report for the best pipeline
- Crop-level ranking tables for performance, yield, and profit proxy

## Environment setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install catboost xgboost lightgbm requests
```

Notes:

- `catboost`, `xgboost`, and `lightgbm` are optional but recommended for full model comparison.
- If optional libraries are not installed, the notebook still runs using available models.

## How to run the model workflow

1. Open `Main Model.ipynb`.
2. Run cells top to bottom.
3. Review the leaderboard and cross-validation summary.
4. Use the final prediction section to inspect ranked crop recommendations.

## Limitations

- Current modeling scope is centered on Thanjavur-driven workflow.
- Target is a proxy label (derived), not a direct ground-truth agronomic outcome label.
- Some paths in notebook cells are absolute Windows paths and may need path normalization.

## Next model improvements

- Add calibrated probabilities (`CalibratedClassifierCV`) for better decision thresholds.
- Add time-aware validation to test temporal robustness.
- Add SHAP-based feature attribution for explainability.
- Export best pipelines (`joblib`) for reuse in an API or dashboard.
- Track experiments with a formal registry (MLflow or similar).
