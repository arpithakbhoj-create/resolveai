
from pathlib import Path
import joblib

# Path to our trained model
MODEL_PATH = (
    Path(__file__).resolve().parent
    / "incident_classifier.joblib"
)

# Load the trained model once
model = joblib.load(MODEL_PATH)


# Predict the category of an IT incident
def predict_incident_category(description: str):

    # Predict category
    prediction = model.predict([description])[0]

    # Get class probabilities
    probabilities = model.predict_proba([description])[0]

    # Find the highest probability
    confidence = float(max(probabilities))

    return {
        "predicted_category": str(prediction),
        "confidence": round(confidence, 4),
        "model_version": "1.0.0"
    }
