import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Preprocessing function
def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # Calculate price per square meter
    df["price_per_sqm"] = df["price"] / df["total_area_sqm"]
    df["price_per_sqm"].replace([float("inf"), float("-inf")], pd.NA)
    df["price_per_sqm"].fillna(df["price_per_sqm"].median())

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
        lambda row: epc_mapping.get(row["region"], {}).get(row["epc"], "MISSING"),
        axis=1
    )

    return df

# Define preprocessor for model features
numeric_to_scale = [
    "construction_year",
    "total_area_sqm",
    "surface_land_sqm",
    "nbr_frontages",
    "nbr_bedrooms",
    "terrace_sqm",
    "garden_sqm",
    "primary_energy_consumption_sqm"
]

binary_flags = [
    "fl_furnished",
    "fl_open_fire",
    "fl_terrace",
    "fl_garden",
    "fl_swimming_pool",
    "fl_floodzone",
    "fl_double_glazing"
]

categorical_cols = [
    "property_type",
    "subproperty_type",
    "region",
    "province",
    "equipped_kitchen",
    "state_building",
    "heating_type",
    "epc_mapped"
]

numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline([
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

binary_transformer = "passthrough"

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_to_scale),
    ("bin", binary_transformer, binary_flags),
    ("cat", categorical_transformer, categorical_cols)
])