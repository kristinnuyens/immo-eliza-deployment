import pandas as pd
import joblib
import sys
import os

# Add src folder to path to load preprocessor if needed
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

# Load preprocessor and model
PREPROCESSOR_PATH = "models/preprocessor.pkl"
MODEL_PATH = "models/model.pkl"

preprocessor = joblib.load(PREPROCESSOR_PATH)
model = joblib.load(MODEL_PATH)

# Prediction-specific preprocessing
def preprocess_for_prediction(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess a dataframe for prediction (no 'price' column expected)."""
    df = df.copy()

    # Map EPC values to standardized categories
    epc_mapping = {
        "Flanders": {"A+": "excellent", "A": "excellent", "B": "good",
                     "C": "poor", "D": "poor", "E": "bad", "F": "bad"},
        "Brussels-Capital": {"A": "excellent", "B": "good", "C": "good",
                             "D": "poor", "E": "poor", "F": "bad", "G": "bad"},
        "Wallonia": {"A++": "excellent", "A+": "excellent", "A": "good",
                     "B": "good", "C": "poor", "D": "poor", "E": "poor",
                     "F": "bad", "G": "bad"}
    }

    df["epc_mapped"] = df.apply(
        lambda row: epc_mapping.get(row["region"], {}).get(row.get("epc", None), "MISSING"),
        axis=1
    )

    return df

def predict(input_data: dict) -> float:
    """
    Predict the price of a property given input data.
    input_data: dict with keys corresponding to features your model expects
    Returns: predicted price as float
    """
    # Convert input dict to DataFrame
    df = pd.DataFrame([input_data])

    # Apply prediction-specific preprocessing
    df_processed = preprocess_for_prediction(df)

    # Drop target column if present
    if "price" in df_processed.columns:
        df_processed = df_processed.drop(columns=["price", "price_per_sqm"])

    # Transform features using preprocessor
    X_processed = preprocessor.transform(df_processed)

    # Predict price
    prediction = model.predict(X_processed)

    return float(prediction[0])