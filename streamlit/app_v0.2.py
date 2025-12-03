import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from api.predict import predict

# --- PAGE SETUP ---
st.set_page_config(page_title="Immo Eliza", page_icon="🏠", layout="wide")
st.title("🏠 Immo Eliza")
st.markdown("### Property Price Predictor")
st.markdown("Fill in the property details below with what you know about your property:")

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

# --- PROPERTY OVERVIEW ---
st.subheader("🏷️ Property Overview")
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
    epc_rating = st.selectbox(
        "EPC Rating (if known)",
        ['A+', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'Unknown'],
        index=8,
        help="If you know your Energy Performance Certificate rating, select it; otherwise leave as Unknown."
    )
    construction_year = st.slider(
        "Construction Year", 1750, 2024, 2000,
        help="Approximate year property was built."
    )

# --- PHYSICAL FEATURES ---
st.subheader("📐 Physical Features")
col1, col2 = st.columns(2)

with col1:
    total_area_sqm = st.number_input(
        "Total Internal Area (sqm, approx.)", min_value=3, max_value=88140, value=100,
        help="Approximate interior living area."
    )
    nbr_bedrooms = st.number_input("Number of Bedrooms", min_value=0, max_value=20, value=3)
    
    # Terrace flag and conditional input
    fl_terrace = st.checkbox("🌿 Terrace")
    if fl_terrace:
        terrace_sqm = st.number_input("Terrace Area (sqm, approx.)", min_value=0, max_value=3466, value=10)
    else:
        terrace_sqm = 0

    # Garden flag and conditional input
    fl_garden = st.checkbox("🌳 Garden")
    if fl_garden:
        garden_sqm = st.number_input("Garden Area (sqm, approx.)", min_value=0, max_value=150000, value=50)
    else:
        garden_sqm = 0

with col2:
    surface_land_sqm = st.number_input(
        "Total Land Area (sqm, approx.)", min_value=0, max_value=950774, value=300,
        help="Total land including garden and terrace."
    )
    nbr_frontages = st.number_input("Number of Frontages", min_value=1, max_value=18, value=2)

# --- AMENITIES ---
st.subheader("✨ Amenities")
col1, col2, col3 = st.columns(3)

with col1:
    fl_furnished = st.checkbox("🏠 Furnished")
    fl_open_fire = st.checkbox("🔥 Open Fire")

with col2:
    fl_swimming_pool = st.checkbox("🏊 Swimming Pool")
    fl_floodzone = st.checkbox("🌊 Flood Zone")

with col3:
    fl_double_glazing = st.checkbox("🪟 Double Glazing")

# --- ADVANCED DETAILS (OPTIONAL) ---
with st.expander("Advanced Property Details (Optional)"):
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
    "property_type": property_type,
    "subproperty_type": subproperty_type,
    "region": region,
    "province": province,
    "epc_rating": epc_rating,
    "construction_year": construction_year,
    "total_area_sqm": total_area_sqm,
    "nbr_bedrooms": nbr_bedrooms,
    "terrace_sqm": terrace_sqm,
    "garden_sqm": garden_sqm,
    "surface_land_sqm": surface_land_sqm,
    "nbr_frontages": nbr_frontages,
    "fl_furnished": fl_furnished,
    "fl_open_fire": fl_open_fire,
    "fl_terrace": fl_terrace,
    "fl_garden": fl_garden,
    "fl_swimming_pool": fl_swimming_pool,
    "fl_floodzone": fl_floodzone,
    "fl_double_glazing": fl_double_glazing,
    "equipped_kitchen": equipped_kitchen,
    "state_building": state_building,
    "heating_type": heating_type
}

# --- PREDICTION BUTTON ---
if st.button("Predict Price"):
    # --- BACKGROUND FIX: inject primary_energy_consumption_sqm ---
    epc_to_energy = {
        'A+': 50, 'A': 75, 'B': 100, 'C': 150, 'D': 200,
        'E': 250, 'F': 300, 'G': 400, 'Unknown': 150
    }
    input_data["primary_energy_consumption_sqm"] = epc_to_energy.get(epc_rating, 150)

    predicted_price = predict(input_data)
    st.markdown(f"""
    <div style="background-color:#FFFAE6;padding:15px;border-radius:10px">
    <h3>💰 Estimated Price: €{predicted_price:,.2f}</h3>
    </div>
    """, unsafe_allow_html=True)
