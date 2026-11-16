
from pathlib import Path
import joblib

# Locate the trained model
MODEL_PATH = (
    Path(__file__).resolve().parent
    / "incident_classifier.joblib"
)

# Load the trained ML pipeline
model = joblib.load(MODEL_PATH)


# New incident descriptions
test_incidents = [
    "Employees cannot connect to VPN from home",

    "SQL queries are taking too long to execute",

    "Suspicious login attempts detected on admin account",

    "Windows server is running out of disk space",

    "Web application crashes after login",

    "Laptop keyboard is not working"
]


# Predict categories
predictions = model.predict(test_incidents)


# Display results
for description, category in zip(
    test_incidents,
    predictions
):
    print("\nIncident:", description)
    print("Predicted Category:", category)

# Examine prediction probabilities
probabilities = model.predict_proba(test_incidents)

# Get all category names
categories = model.classes_

print("\n--- Prediction Confidence Analysis ---")

for description, predicted, probability in zip(
    test_incidents,
    predictions,
    probabilities
):
    confidence = max(probability) * 100

    print(f"\nIncident: {description}")
    print(f"Prediction: {predicted}")
    print(f"Confidence: {confidence:.2f}%")

    # Show the top 3 predicted categories
    ranked_indices = probability.argsort()[::-1][:3]

    print("Top 3 categories:")

    for index in ranked_indices:
        print(
            f"  {categories[index]}: "
            f"{probability[index] * 100:.2f}%"
        )
