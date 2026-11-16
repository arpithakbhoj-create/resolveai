
from pathlib import Path

import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "ml" / "incident_classifier.joblib"
EVALUATION_PATH = BASE_DIR / "data" / "evaluation.csv"

# Load trained model and independent evaluation data
model = joblib.load(MODEL_PATH)
data = pd.read_csv(EVALUATION_PATH)

# Separate descriptions and actual categories
X = data["description"]
y_true = data["category"]

# Generate predictions
y_pred = model.predict(X)

# Calculate evaluation metrics
accuracy = accuracy_score(y_true, y_pred)

print("\n--- Independent Evaluation Results ---")
print(f"Total evaluation incidents: {len(data)}")
print(f"Accuracy: {accuracy:.2%}")

print("\nClassification Report:")
print(
    classification_report(
        y_true,
        y_pred,
        zero_division=0
    )
)

print("\nIndividual Predictions:")

for description, actual, predicted in zip(
    X,
    y_true,
    y_pred
):
    result = "CORRECT" if actual == predicted else "INCORRECT"

    print(f"\nIncident: {description}")
    print(f"Actual: {actual}")
    print(f"Predicted: {predicted}")
    print(f"Result: {result}")

print("\nConfusion Matrix:")

categories = sorted(y_true.unique())

matrix = confusion_matrix(
    y_true,
    y_pred,
    labels=categories
)

print("Category order:", categories)
print(matrix)
