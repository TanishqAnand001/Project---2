Tamil Nadu Crop Recommendation System (AI/ML Capstone Project)
Project Overview

This project is an AI/ML-based Crop Recommendation System designed specifically for Tamil Nadu, leveraging region-centric soil and climate data. Unlike generic crop recommendation systems, this model is trained on Tamil Nadu district-level data, making its predictions locally relevant and agriculturally meaningful.

The system predicts the most suitable crops based on soil nutrients and seasonal climatic conditions using a Random Forest classifier, enhanced with data augmentation and model explainability (SHAP).

Key Objectives

Build a region-specific crop recommendation model for Tamil Nadu

Integrate real weather data with soil survey data

Ensure robust machine learning practices (no data leakage, proper validation)

Provide interpretable crop recommendations

Recommend top-3 crops with probability scores

Region of Focus

Tamil Nadu, India

District-level data is used with latitude and longitude mapping to ensure accurate weather retrieval and regional specificity.

Dataset Description
Features

The final dataset contains the following features:

Feature	Description
District	Tamil Nadu district name
N	Nitrogen content in soil
P	Phosphorus content in soil
K	Potassium content in soil
pH	Soil pH value
Temperature	Seasonal average temperature (°C)
Rainfall	Seasonal total rainfall (mm)
Humidity	Seasonal average humidity (%)
Crop (Label)	Recommended crop
Time Span

2020 – 2025

Approximately 2000 records

Five years of data

Data Collection Methodology
Weather Data

Weather data was collected using real APIs based on district latitude and longitude:

Open-Meteo API

NASA POWER API

Weather data was collected daily and aggregated into seasonal averages for:

Kharif

Rabi

Summer

Soil Data

Soil data was sourced from surveys conducted by Tamil Nadu Agricultural University (TNAU). These surveys provide scientifically measured soil nutrient values for Tamil Nadu districts.

Crop Label Generation

Crop labels were generated using a knowledge-based approach:

A generic crop recommendation dataset was used as a reference

Soil and climate conditions were mapped to suitable crops using domain knowledge

This ensures realistic crop-condition relationships in the dataset.

Data Preprocessing

Removal of null values, duplicates, and missing data

Label encoding for categorical variables

Feature scaling where required

Clean dataset prepared for machine learning training

Machine Learning Model
Random Forest Crop Recommendation Model

A Random Forest Classifier was used as the core model due to its ability to learn non-linear relationships, robustness to noise, and interpretability through feature importance.

Model Specialties
Data Augmentation

Training data was augmented ten times by applying small random variations to numerical features. This improves the model’s ability to generalize to real-world variations.

No Data Leakage

The train-test split was performed before data augmentation. The test dataset remains untouched, ensuring unbiased evaluation.

Regional Relevance

The model is trained on Tamil Nadu-specific synthetic crop data, making predictions relevant to local agricultural conditions.

Explainable AI (SHAP)

SHAP analysis is used to understand the influence of soil nutrients and climate factors such as nitrogen, phosphorus, potassium, temperature, rainfall, humidity, and pH on crop recommendations.

Top-3 Crop Recommendations

The recommendation function returns the top three crops along with their probability scores, providing multiple viable options instead of a single prediction.

Optimized Hyperparameters

Number of trees: 300

Maximum depth: 18

These values balance predictive performance and computational efficiency.

Model Performance

Current accuracy: approximately 82 percent

Evaluation performed on clean, non-augmented test data

Input Features Used

Soil nutrients: N, P, K

Climate factors: Temperature, Humidity, Rainfall

Soil property: pH

Current Limitations

Stress conditions such as drought and famine are not yet modeled

Explainable AI implementation can be improved

Dataset size is limited

Only Random Forest has been extensively explored

Future Work

Incorporate stress conditions such as drought, flood, and famine

Improve Explainable AI (XAI) depth and visualization

Expand the dataset with more years and districts

Experiment with advanced models such as XGBoost, LightGBM, and neural networks

Implement a complete end-to-end crop recommendation pipeline

Deploy the system as a web or mobile application

Project Novelty

Tamil Nadu district-centric dataset

Real-time weather data collected from public APIs

Seasonal aggregation aligned with Indian cropping patterns

Strong emphasis on machine learning best practices

Integration of domain knowledge with AI

Project Type

AI/ML Capstone Project

Author

Tanishq Anand
