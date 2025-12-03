import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingRegressor
from preprocess_module import preprocess, preprocessor

# Paths
DATA_PATH = "data/immo_data_subset.csv"
PREPROCESSOR_PATH = "models/preprocessor.pkl"
MODEL_PATH = "models/model.pkl"

# Load dataset
df = pd.read_csv(DATA_PATH)

# Preprocess dataframe
df_processed = preprocess(df)

# Define target and features
y = df_processed["price"]
X = df_processed.drop(columns=["price", "price_per_sqm"])

# Fit preprocessor
preprocessor.fit(X)
X_processed = preprocessor.transform(X)

# Save preprocessor
joblib.dump(preprocessor, PREPROCESSOR_PATH)
print(f"Preprocessor saved to: {PREPROCESSOR_PATH}")

# Train model
model = GradientBoostingRegressor()
model.fit(X_processed, y)

# Save trained model
joblib.dump(model, MODEL_PATH)
print(f"Model saved to: {MODEL_PATH}")