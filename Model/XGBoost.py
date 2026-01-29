import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

# -------------------------------------------------
# 1. Load SOFT-LABEL dataset
# -------------------------------------------------
data = pd.read_csv("../data/tn_synthetic_crop_data.csv")

features = ["N", "P", "K", "Temperature", "Humidity", "pH", "Rainfall"]
X = data[features]
y = data["crop"]

# -------------------------------------------------
# 2. Encode labels (REQUIRED for XGBoost)
# -------------------------------------------------
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# -------------------------------------------------
# 3. Train-test split (before augmentation)
# -------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded,
    test_size=0.2,
    stratify=y_encoded,
    random_state=42
)

# -------------------------------------------------
# 4. Augment ONLY training data
# -------------------------------------------------
train_df = X_train.copy()
train_df["crop"] = y_train

augmented = []

for _, row in train_df.iterrows():
    for _ in range(10):
        r = row.copy()
        r["Temperature"] += np.random.normal(0, 1.0)
        r["Rainfall"] += np.random.normal(0, 12)
        r["Humidity"] += np.random.normal(0, 3)
        r["N"] += np.random.normal(0, 4)
        r["P"] += np.random.normal(0, 2)
        r["K"] += np.random.normal(0, 2)
        augmented.append(r)

aug_train = pd.DataFrame(augmented)

X_train_aug = aug_train[features]
y_train_aug = aug_train["crop"]

# -------------------------------------------------
# 5. Train XGBoost model
# -------------------------------------------------
model = XGBClassifier(
    n_estimators=600,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.85,
    colsample_bytree=0.85,
    objective="multi:softprob",
    eval_metric="mlogloss",
    random_state=42
)

model.fit(X_train_aug, y_train_aug)

# -------------------------------------------------
# 6. Evaluate on unseen test set
# -------------------------------------------------
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    )
)
