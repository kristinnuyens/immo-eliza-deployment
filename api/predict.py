import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

# Preprocessing function
def preprocess(df, fit=True, preprocessor=None):
    df_copy = df.copy()
    
    # Assuming you have a defined target column 'price'
    df_copy['price_per_sqm'] = df_copy['price'] / df_copy['total_area_sqm']
    df_copy['price_per_sqm'].replace([np.inf, -np.inf], np.nan, inplace=True)

    epc_mapping = {
        "Flanders": {"A+": "excellent", "A": "excellent", "B": "good",
                     "C": "poor", "D": "poor", "E": "bad", "F": "bad"},
        "Brussels-Capital": {"A": "excellent", "B": "good", "C": "good",
                             "D": "poor", "E": "poor", "F": "bad", "G": "bad"},
        "Wallonia": {"A++": "excellent", "A+": "excellent", "A": "good",
                     "B": "good", "C": "poor", "D": "poor", "E": "poor",
                     "F": "bad", "G": "bad"}
    }
    df_copy['epc_recoded'] = df_copy.apply(
        lambda row: epc_mapping.get(row['region'], {}).get(row['epc'], 'MISSING'),
        axis=1
    )

    binary_flags = ['fl_furnished', 'fl_open_fire', 'fl_terrace',
                    'fl_garden', 'fl_swimming_pool', 'fl_floodzone', 'fl_double_glazing']
    numeric_to_scale = ['construction_year', 'total_area_sqm', 'surface_land_sqm',
                        'nbr_frontages', 'terrace_sqm', 'garden_sqm',
                        'primary_energy_consumption_sqm', 'nbr_bedrooms', 'price_per_sqm']
    categorical_cols = ['property_type', 'subproperty_type', 'region', 'province',
                        'equipped_kitchen', 'state_building', 'heating_type', 'epc_recoded']

    continuous_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    binary_transformer = 'passthrough'
    categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

    if preprocessor is None and fit:
        preprocessor = ColumnTransformer(transformers=[
            ('num_scaled', continuous_transformer, numeric_to_scale),
            ('bin_flags', binary_transformer, binary_flags),
            ('cat', categorical_transformer, categorical_cols)
        ], remainder='passthrough')

    if fit:
        X_transformed = preprocessor.fit_transform(df_copy)
    else:
        X_transformed = preprocessor.transform(df_copy)

    cat_features = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_cols)
    scaled_features = [f"{col}_scaled" for col in numeric_to_scale]
    all_features = scaled_features + binary_flags + cat_features.tolist() + \
                   [col for col in df_copy.columns if col not in numeric_to_scale + binary_flags + categorical_cols]

    df_final = pd.DataFrame(X_transformed, columns=all_features)

    df_numeric = df_final.apply(pd.to_numeric, errors='coerce')
    df_numeric = df_numeric.fillna(df_numeric.median())

    columns_to_drop = [
        'id', 'construction_year', 'total_area_sqm', 'surface_land_sqm', 'property_type',
        'subproperty_type', 'nbr_frontages', 'terrace_sqm', 'garden_sqm', 'primary_energy_consumption_sqm',
        'nbr_bedrooms', 'price_per_sqm', 'epc', 'locality'
    ]
    df_ready = df_numeric.drop(columns=[col for col in columns_to_drop if col in df_numeric.columns])

    return df_ready, preprocessor

def predict_price(df_ready, model_path):
    # Load the pre-trained model (your best model)
    model = joblib.load(model_path)
    
    # Dropping any target or unrelated columns
    X_test = df_ready.drop(columns=['price'], errors='ignore')
    
    # Predict using the best model
    y_pred = model.predict(X_test)
    
    return y_pred

if __name__ == "__main__":
    # Gather the input data
    input_path = input("Enter the path to the input CSV file: ")

    # Load the input data
    df = pd.read_csv(input_path)
    
    # Preprocess data
    df_ready, preprocessor = preprocess(df, fit=True)

    # Make predictions
    y_pred = predict_price(df_ready, model_path="../api/xgboost_model.pkl")

    # Display the prediction results
    print("Predicted price:")
    for i, price in enumerate(y_pred, start=1):
        print(f"Property {i}: {price:.2f}")