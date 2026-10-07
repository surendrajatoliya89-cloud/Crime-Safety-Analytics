import json
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

print("=" * 65)
print("MULTI-YEAR CRIME RISK PREDICTION MODEL TRAINING (2021-2024)")
print("=" * 65)

# 1. Load Cleaned Dataset
df = pd.read_csv("data/crime_data_clean.csv")
print(f"Loaded dataset with {len(df)} records spanning years {sorted(df['Year'].unique().tolist())}.")

# 2. Define Features (X) and Target (y)
categorical_features = [
    "State", "City", "Area", "Crime_Type", "Month", "Day_of_Week", 
    "Time_Category", "Weather", "Holiday", "Location_Type"
]
numerical_features = ["Year", "Previous_Incidents"]

target_col = "Crime_Risk_Level"

X = df[categorical_features + numerical_features]
y = df[target_col]

print(f"Features selected ({len(categorical_features) + len(numerical_features)}): {categorical_features + numerical_features}")
print(f"Target classes: {sorted(y.unique().tolist())}")

# 3. Train-Test Split (80/20 stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
print(f"Training records: {len(X_train)} | Testing records: {len(X_test)}")

# 4. Pipeline with ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
        ("num", StandardScaler(), numerical_features)
    ]
)

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42))
])

# 5. Train
print("\nTraining Random Forest Classifier on multi-year data...")
pipeline.fit(X_train, y_train)
print("Training complete!")

# 6. Evaluate
y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average="weighted")
recall = recall_score(y_test, y_pred, average="weighted")
f1 = f1_score(y_test, y_pred, average="weighted")
conf_matrix = confusion_matrix(y_test, y_pred, labels=["Low", "Medium", "High"])

print("\n--- MODEL PERFORMANCE ON TEST DATA ---")
print(f"Accuracy  : {accuracy * 100:.2f}%")
print(f"Precision : {precision * 100:.2f}%")
print(f"Recall    : {recall * 100:.2f}%")
print(f"F1 Score  : {f1 * 100:.2f}%")

print("\n--- CONFUSION MATRIX (Rows: Actual [Low, Medium, High], Cols: Predicted) ---")
print(conf_matrix)

# 7. Save Model Pipeline & Metrics
os.makedirs("model", exist_ok=True)
model_file_path = os.path.join("model", "crime_risk_model.pkl")
joblib.dump(pipeline, model_file_path)
print(f"\nModel pipeline successfully saved to '{model_file_path}'")

metrics_summary = {
    "accuracy": round(accuracy * 100, 2),
    "precision": round(precision * 100, 2),
    "recall": round(recall * 100, 2),
    "f1_score": round(f1 * 100, 2),
    "classes": ["Low", "Medium", "High"],
    "confusion_matrix": conf_matrix.tolist()
}

with open(os.path.join("model", "model_metrics.json"), "w") as f:
    json.dump(metrics_summary, f, indent=4)
print("Model metrics saved to 'model/model_metrics.json'")
print("=" * 65)
