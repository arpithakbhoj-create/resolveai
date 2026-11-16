
from pathlib import Path

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report


# Define project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "data" / "incidents.csv"
MODEL_PATH = BASE_DIR / "ml" / "incident_classifier.joblib"


# Step 1: Load the dataset
data = pd.read_csv(DATASET_PATH)

print("Dataset loaded successfully")
print(f"Total incidents: {len(data)}")


# Step 2: Separate input and output
X = data["description"]
y = data["category"]


# Step 3: Split into training and testing datasets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

print(f"Training incidents: {len(X_train)}")
print(f"Testing incidents: {len(X_test)}")


# Step 4: Create the ML pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            random_state=42,
            class_weight="balanced"
        )
    )
])


# Step 5: Train the model
model.fit(X_train, y_train)

print("\nModel training completed successfully")


# Step 6: Evaluate the model
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"\nModel Accuracy: {accuracy:.2%}")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# Step 7: Save the trained model
joblib.dump(model, MODEL_PATH)

print(f"\nModel saved successfully: {MODEL_PATH}")
