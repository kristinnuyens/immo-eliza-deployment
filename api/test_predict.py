# test_predict.py
from predict import predict

# Sample input for one property (fill in values as appropriate)
sample_input = {
    "construction_year": 2005,
    "total_area_sqm": 120,
    "surface_land_sqm": 300,
    "nbr_frontages": 2,
    "nbr_bedrooms": 3,
    "terrace_sqm": 15,
    "garden_sqm": 100,
    "primary_energy_consumption_sqm": 150,
    "fl_furnished": False,
    "fl_open_fire": True,
    "fl_terrace": True,
    "fl_garden": True,
    "fl_swimming_pool": False,
    "fl_floodzone": False,
    "fl_double_glazing": True,
    "property_type": "HOUSE",
    "subproperty_type": "HOUSE",
    "region": "Flanders",
    "province": "Antwerp",
    "equipped_kitchen": "installed",
    "state_building": "good",
    "heating_type": "FUELOIL",
    "epc_mapped": "good"  # Optional; preprocess will remap anyway
}

# Call the predict function
predicted_price = predict(sample_input)

print(f"Predicted price: €{predicted_price:,.2f}")