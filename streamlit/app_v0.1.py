import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from api.predict import predict

# --- PAGE SETUP ---
st.set_page_config(page_title="Immo Eliza", page_icon="🏠", layout="wide")
st.title("🏠 Immo Eliza")
st.markdown("### Property Price Predictor")
st.markdown("Fill in the property details below to get an estimated price:")

# --- STYLING BUTTON ---
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #4CAF50;
    color: white;
    font-size: 18px;
    height: 50px;
    width: 100%;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- NUMERIC FEATURES ---
st.subheader("📊 Numeric Features")
col1, col2 = st.columns(2)

with col1:
    construction_year = st.number_input("Construction Year", min_value=1753, max_value=2024, value=2000)
    total_area_sqm = st.number_input("Total Area (sqm)", min_value=3, max_value=88140, value=100)
    surface_land_sqm = st.number_input("Surface Land (sqm)", min_value=0, max_value=950774, value=300)
    nbr_frontages = st.number_input("Number of Frontages", min_value=1, max_value=18, value=2)

with col2:
    nbr_bedrooms = st.number_input("Number of Bedrooms", min_value=0, max_value=100, value=3)
    terrace_sqm = st.number_input("Terrace Area (sqm)", min_value=0, max_value=3466, value=10)
    garden_sqm = st.number_input("Garden Area (sqm)", min_value=0, max_value=150000, value=50)
    primary_energy_consumption_sqm = st.number_input(
        "Primary Energy Consumption (kWh/m²)", min_value=-99, max_value=20231122, value=150
    )

# --- BINARY FEATURES ---
st.subheader("✨ Amenities")
col1, col2, col3 = st.columns(3)

with col1:
    fl_furnished = st.checkbox("🏠 Furnished")
    fl_open_fire = st.checkbox("🔥 Open Fire")

with col2:
    fl_terrace = st.checkbox("🌿 Terrace")
    fl_garden = st.checkbox("🌳 Garden")

with col3:
    fl_swimming_pool = st.checkbox("🏊 Swimming Pool")
    fl_floodzone = st.checkbox("🌊 Flood Zone")
    fl_double_glazing = st.checkbox("🪟 Double Glazing")

# --- CATEGORICAL FEATURES ---
st.subheader("🏷️ Property Details")
col1, col2 = st.columns(2)

with col1:
    property_type = st.selectbox("Property Type", ['HOUSE', 'APARTMENT'])
    subproperty_type = st.selectbox("Subproperty Type", [
        'HOUSE', 'APARTMENT', 'DUPLEX', 'FLAT_STUDIO', 'APARTMENT_BLOCK',
        'MIXED_USE_BUILDING', 'GROUND_FLOOR', 'PENTHOUSE', 'BUNGALOW', 'VILLA',
        'LOFT', 'TOWN_HOUSE', 'KOT', 'OTHER_PROPERTY', 'MANSION', 'CHALET',
        'TRIPLEX', 'SERVICE_FLAT', 'EXCEPTIONAL_PROPERTY', 'FARMHOUSE', 'MANOR_HOUSE',
        'COUNTRY_COTTAGE', 'CASTLE'
    ])
    region = st.selectbox("Region", ['Flanders', 'Brussels-Capital', 'Wallonia', 'MISSING'])
    province = st.selectbox("Province", [
        'Flemish Brabant', 'East Flanders', 'Brussels', 'Walloon Brabant', 'Namur',
        'Liège', 'West Flanders', 'Antwerp', 'Luxembourg', 'Hainaut', 'Limburg', 'MISSING'
    ])

with col2:
    with st.expander("Advanced Property Details"):
        equipped_kitchen = st.selectbox("Equipped Kitchen", [
            'HYPER_EQUIPPED', 'INSTALLED', 'USA_HYPER_EQUIPPED', 'MISSING',
            'SEMI_EQUIPPED', 'NOT_INSTALLED', 'USA_SEMI_EQUIPPED', 'USA_INSTALLED', 'USA_UNINSTALLED'
        ])
        state_building = st.selectbox("State of Building", [
            'GOOD', 'MISSING', 'AS_NEW', 'JUST_RENOVATED', 'TO_RENOVATE', 'TO_BE_DONE_UP', 'TO_RESTORE'
        ])
        heating_type = st.selectbox("Heating Type", [
            'FUELOIL', 'GAS', 'MISSING', 'ELECTRIC', 'WOOD', 'PELLET', 'SOLAR', 'CARBON'
        ])

# --- COLLECT INPUTS ---
input_data = {
    "construction_year": construction_year,
    "total_area_sqm": total_area_sqm,
    "surface_land_sqm": surface_land_sqm,
    "nbr_frontages": nbr_frontages,
    "nbr_bedrooms": nbr_bedrooms,
    "terrace_sqm": terrace_sqm,
    "garden_sqm": garden_sqm,
    "primary_energy_consumption_sqm": primary_energy_consumption_sqm,
    "fl_furnished": fl_furnished,
    "fl_open_fire": fl_open_fire,
    "fl_terrace": fl_terrace,
    "fl_garden": fl_garden,
    "fl_swimming_pool": fl_swimming_pool,
    "fl_floodzone": fl_floodzone,
    "fl_double_glazing": fl_double_glazing,
    "property_type": property_type,
    "subproperty_type": subproperty_type,
    "region": region,
    "province": province,
    "equipped_kitchen": equipped_kitchen,
    "state_building": state_building,
    "heating_type": heating_type
}

# --- PREDICTION BUTTON ---
if st.button("Predict Price"):
    predicted_price = predict(input_data)
    st.markdown(f"""
    <div style="background-color:#FFFAE6;padding:15px;border-radius:10px">
    <h3>💰 Estimated Price: €{predicted_price:,.2f}</h3>
    </div>
    """, unsafe_allow_html=True)
