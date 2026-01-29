import pandas as pd
import shap
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def recommend_crop(input_data, model):
    probs = model.predict_proba([input_data])[0]
    crops = model.classes_
    results = sorted(zip(crops, probs), key=lambda x: x[1], reverse=True)
    return results[:3]


data = pd.read_csv("../data/tn_augmented_crop_data.csv")

features = ["N", "P", "K", "Temperature", "Humidity", "pH", "Rainfall"]
X = data[features]
y = data["crop"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=18,
    random_state=42
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

shap.summary_plot(shap_values, X)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

