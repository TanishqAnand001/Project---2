import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

# -------------------------------------------------
# 1. Load datasets
# -------------------------------------------------
kaggle = pd.read_csv("../data/Crop_recommendation.csv")
soil = pd.read_csv("../data/average_soil_nutrients_tn_districtwise.csv")
climate = pd.read_csv("../data/tn_climate_10years_seasonal.csv")

print("SOIL COLUMNS (repr):")
for c in soil.columns:
    print(repr(c))

print("\nCLIMATE COLUMNS (repr):")
for c in climate.columns:
    print(repr(c))

print("\nChecks:")
print("District in soil:", "District" in soil.columns)
print("District in climate:", "District" in climate.columns)

print("Soil index name:", soil.index.name)
print("Climate index name:", climate.index.name)

print("Unique soil districts (sample):")
print([repr(x) for x in soil["District"].unique()[:10]])

print("\nUnique climate districts (sample):")
print([repr(x) for x in climate["District"].unique()[:10]])


# -------------------------------------------------
# 2. Normalize column names
# -------------------------------------------------
for df in [kaggle, soil, climate]:
    df.columns = df.columns.str.strip().str.lower()

soil = soil.rename(columns={
    "N": "N",
    "P": "P",
    "K": "K",
    "pH": "pH"
})

climate = climate.rename(columns={
    "Temperature": "Temperature",
    "Humidity": "Humidity",
    "Rainfall": "Rainfall"
})

# -------------------------------------------------
# 3. Merge Tamil Nadu soil + climate
# -------------------------------------------------
tn = soil.merge(climate, on="District")

features = ["N", "P", "K", "Temperature", "Humidity", "pH", "Rainfall"]

# -------------------------------------------------
# 4. Scale features
# -------------------------------------------------
scaler = StandardScaler()
kaggle_scaled = scaler.fit_transform(kaggle[features])
tn_scaled = scaler.transform(tn[features])

# -------------------------------------------------
# 5. Cosine similarity
# -------------------------------------------------
similarity = cosine_similarity(tn_scaled, kaggle_scaled)

# -------------------------------------------------
# 6. SOFT-LABEL assignment
# -------------------------------------------------
K = 40
confidence_threshold = 0.6
labels = []
confidences = []

for i in range(similarity.shape[0]):
    top_k_idx = similarity[i].argsort()[-K:]
    top_crops = kaggle.iloc[top_k_idx]["label"]

    counts = Counter(top_crops)
    crop, freq = counts.most_common(1)[0]
    confidence = freq / K

    if confidence >= confidence_threshold:
        labels.append(crop)
        confidences.append(confidence)
    else:
        labels.append("uncertain")
        confidences.append(confidence)

tn["crop"] = labels
tn["confidence"] = confidences

# -------------------------------------------------
# 7. Remove low-confidence rows
# -------------------------------------------------
tn = tn[tn["crop"] != "uncertain"].reset_index(drop=True)

# -------------------------------------------------
# 8. Save clean synthetic dataset
# -------------------------------------------------
tn.to_csv("../data/tn_softlabel_crop_data.csv", index=False)

print("Soft-label TN dataset created")
print("Final shape:", tn.shape)
print("Average confidence:", tn["confidence"].mean())
