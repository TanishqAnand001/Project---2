# Tamil Nadu Crop Recommendation System (AI/ML Capstone Project)

## Project Overview

This project is an AI/ML-based Crop Recommendation System designed specifically for Tamil Nadu, leveraging region-centric soil and climate data. Unlike generic crop recommendation systems, this model is trained on Tamil Nadu district-level data, making its predictions locally relevant and agriculturally meaningful.

The system predicts the most suitable crops based on soil nutrients and seasonal climatic conditions using a Random Forest classifier, enhanced with data augmentation and model explainability (SHAP).

---

## Key Objectives

* Build a region-specific crop recommendation model for Tamil Nadu
* Integrate real weather data with soil survey data
* Reduce dependence on generalized, non-local datasets
* Ensure robust machine learning practices (no data leakage, proper validation)
* Provide interpretable and reliable crop recommendations
* Recommend top-3 crops with probability scores

---

## Region of Focus

Tamil Nadu, India

District-level data is used with latitude and longitude mapping to ensure accurate weather retrieval and regional specificity.

---

## Dataset Description

### Features

The final dataset contains the following features:

| Feature      | Description                       |
| ------------ | --------------------------------- |
| District     | Tamil Nadu district name          |
| N            | Nitrogen content in soil          |
| P            | Phosphorus content in soil        |
| K            | Potassium content in soil         |
| pH           | Soil pH value                     |
| Temperature  | Seasonal average temperature (°C) |
| Rainfall     | Seasonal total rainfall (mm)      |
| Humidity     | Seasonal average humidity (%)     |
| Crop (Label) | Recommended crop                  |

---

### Time Span

* 2020 – 2025
* Approximately 2000 records
* Five years of data

---

## Data Collection Methodology

### Weather Data

Weather data was collected using real APIs based on district latitude and longitude:

* Open-Meteo API
* NASA POWER API

Daily weather observations were aggregated into seasonal climate summaries for:

* Kharif
* Rabi
* Summer

---

### Soil Data

Soil data was sourced from surveys conducted by Tamil Nadu Agricultural University (TNAU), providing scientifically validated soil nutrient measurements.

---

### Crop Label Generation

Crop labels were generated using a knowledge-based mapping approach:

* Generic crop recommendation datasets were used only as a reference
* Soil and climate parameters were mapped to suitable crops using domain knowledge

This approach minimizes blind reliance on generalized datasets and improves agronomic realism.

---

## Data Preprocessing

* Removal of null values, duplicates, and missing records
* Label encoding for categorical features
* Feature normalization where required
* Clean dataset prepared for machine learning pipelines

---

## Machine Learning Model

### Random Forest Crop Recommendation Model

A Random Forest Classifier was chosen for its ability to model complex non-linear relationships, robustness to noisy agricultural data, and inherent feature importance estimation.

---

### Model Specialties

#### Data Augmentation

Training data was augmented ten times using controlled random perturbations of numerical features. This simulates real-world variability in soil and weather conditions and improves generalization.

#### No Data Leakage

The dataset was split into training and testing sets prior to augmentation, ensuring that evaluation is performed on untouched, realistic data.

#### Regional Relevance

The model is trained exclusively on Tamil Nadu-specific crop data, improving its suitability for local agricultural decision-making.

#### Explainable AI (SHAP)

SHAP-based explanations are incorporated to identify how soil nutrients and climatic variables influence crop recommendations. This supports transparency and interpretability, which are often missing in existing crop recommendation systems.

#### Top-3 Crop Recommendations

Instead of producing a single output, the system returns the top three most suitable crops along with confidence scores, enabling informed decision-making under uncertainty.

#### Optimized Hyperparameters

* Number of trees: 300
* Maximum depth: 18

These parameters were selected to balance model accuracy and computational efficiency.

---

## Model Performance

* Current accuracy: approximately 82 percent
* Performance evaluated on a clean, non-augmented test dataset

---

## Identified Research Gaps Addressed

### 1. Lack of Tamil Nadu–Centric Studies

Most existing crop recommendation research relies on pan-India or global datasets. There are very few studies that focus exclusively on Tamil Nadu, despite its diverse agro-climatic zones. This project directly addresses this gap by constructing and using a Tamil Nadu district-level dataset.

### 2. Over-Reliance on Generalized Datasets

Many published models use generic crop recommendation datasets that ignore regional soil and climate variability. This project reduces dependence on such datasets by integrating real weather data and locally sourced soil surveys, making the model context-aware.

### 3. Absence of Stress Condition Modeling

Existing systems rarely consider agricultural stress conditions such as drought, famine, or abnormal rainfall. Most models provide static recommendations. This project explicitly identifies the lack of stress-aware crop recommendation and proposes alternate crop suggestions as a key area for future enhancement.

### 4. Limited Use of Explainable AI in Agriculture

Although machine learning models are increasingly used in agriculture, explainability is often neglected. This project highlights the gap in Explainable AI adoption and integrates SHAP analysis to make crop recommendations transparent and interpretable.

---

## Current Limitations

* Stress conditions such as drought and famine are not yet explicitly modeled
* Explainable AI implementation can be expanded with deeper visual analysis
* Dataset size is limited and can be further scaled
* Only Random Forest has been fully explored

---

## Future Work

* Incorporate climate stress indicators such as drought indices and extreme rainfall events
* Develop alternate crop recommendation strategies under stress conditions
* Enhance Explainable AI with farmer-friendly visual dashboards
* Expand dataset coverage across more years and micro-regions
* Evaluate advanced models such as XGBoost, LightGBM, and deep learning architectures
* Deploy the system as a web or mobile-based decision support tool

---

## Project Novelty

* Tamil Nadu–centric, district-level dataset
* Real weather data collected via public APIs
* Seasonal aggregation aligned with Indian cropping cycles
* Stress-aware crop recommendation identified as a research direction
* Strong emphasis on model transparency and ML best practices

---

## Project Type

AI/ML Capstone Project

---

## Author

Tanishq Anand
