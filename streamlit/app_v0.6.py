import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime
import streamlit as st
from PIL import Image
from api.predict import predict

# --- PAGE SETUP ---
st.set_page_config(page_title="Immo Eliza - Belgian Property Price Predictor", page_icon="🏠", layout="wide")

# --- GLOBAL STYLES ---
st.markdown("""
<style>
.main .block-container { padding-top: 0rem; }

/* Button style */
div.stButton > button:first-child {
    background-color: #4CAF50;
    color: white;
    font-size: 18px;
    height: 50px;
    width: 100%;
    border-radius: 10px;
}

/* Inputs */
input[type="number"], select, input[type="text"] {
    border: 1px solid #888;
    border-radius: 5px;
    padding: 4px;
}
""", unsafe_allow_html=True)

# --- LOAD LOGO ---
logo_path = os.path.join(os.path.dirname(__file__), "..", "src", "Immo_Eliza_Logo.png")
logo = Image.open(logo_path)

# --- TITLE WITH LOGO ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image(logo, width=190)
with col2:
    st.markdown("""
        <div style='margin-top:-25px;'>
            <h1 style='margin:0;'>Immo Eliza</h1>
            <h2 style='margin-top:2px;'>Belgian Property Price Predictor</h2>
            <p style='margin:4px 0 0 0;'>Fill in the known details to get your property price prediction:</p>
            <p style='font-size: 0.8rem; color: #666;'>(Fields marked with * are required)</p>
        </div>
    """, unsafe_allow_html=True)

# --- CALCULATE CURRENT YEAR ---
current_year = datetime.now().year

# --- PROPERTY DETAILS ---
st.markdown("<h3 style='font-size:20px; margin-bottom:1px;'>🏷️ Details</h3>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="required-section">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    property_type_map = {"HOUSE": "House", "APARTMENT": "Apartment"}
    subproperty_mapping = {
        "Apartment": ["Apartment","Duplex","Flat Studio","Ground Floor","Kot","Loft","Penthouse","Service Flat","Triplex"],
        "House": ["Apartment Block","Bungalow","Castle","Chalet","Country Cottage","Exceptional Property","Farmhouse","House",
                  "Manor House","Mansion","Mixed Use Building","Other Property","Town House","Villa"]
    }
    region_province_map = {
        "Flanders": ["Flemish Brabant","East Flanders","West Flanders","Antwerp","Limburg"],
        "Brussels-Capital": ["Brussels"],
        "Wallonia": ["Walloon Brabant","Namur","Liège","Luxembourg","Hainaut"],
        "MISSING": ["MISSING"]
    }
    state_building_map = {
        "AS_NEW": "As New","JUST_RENOVATED": "Just Renovated","GOOD": "Good",
        "TO_BE_DONE_UP": "To be Done Up","TO_RESTORE": "To Restore","TO_RENOVATE": "To Renovate",
        "MISSING": "Missing"
    }

    with col1:
        property_type = st.selectbox("Property Type *", list(property_type_map.values()))
        subproperty_choices = subproperty_mapping.get(property_type, ["Other"])
        subproperty_type = st.selectbox("Subproperty Type *", sorted(subproperty_choices))
        region = st.selectbox("Region *", sorted(region_province_map.keys()))
        province_choices = region_province_map.get(region, ["MISSING"])
        province = st.selectbox("Province *", sorted(province_choices))

    with col2:
        zip_code = st.text_input("ZIP Code")
        state_building = st.selectbox("State of Building *", list(state_building_map.values()))
        nbr_bedrooms = st.number_input("Number of Bedrooms *", min_value=0, max_value=20, value=2)
        nbr_frontages = st.number_input("Number of Frontages *", min_value=1, max_value=18, value=2)

    with col3:
        total_area_sqm = st.number_input("Internal Area (sqm) *", min_value=8, max_value=100000, value=180)
        surface_land_sqm = st.number_input("Land Area (sqm) *", min_value=0, max_value=1000000, value=200)
        construction_year = st.number_input("Construction Year *", min_value=1750, max_value=current_year, value=2000)
        epc_rating = st.selectbox("EPC Rating", ["A+","A","B","C","D","E","F","G","Unknown"], index=8)

    st.markdown("</div>", unsafe_allow_html=True)

# --- AMENITIES ---
st.markdown("<h3 style='font-size:20px; margin-bottom:1px;'>✨ Amenities</h3>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="required-section">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        fl_double_glazing = st.checkbox("🪟 Double Glazing")
        fl_open_fire = st.checkbox("🔥 Open Fire")

    with col2:
        fl_swimming_pool = st.checkbox("🏊 Swimming Pool")
        fl_furnished = st.checkbox("🏠 Furnished")

    with col3:
        equipped_kitchen_map = {"Equipped":"EQUIPPED","Partially Equipped":"PARTIALLY_EQUIPPED","Not Equipped":"NOT_EQUIPPED","Unknown":"UNKNOWN"}
        equipped_kitchen = st.selectbox("👩🏼‍🍳 Equipped Kitchen", list(equipped_kitchen_map.keys()))

    st.markdown("</div>", unsafe_allow_html=True)

# --- CHARACTERISTICS ---
st.markdown("<h3 style='font-size:20px; margin-bottom:1px;'>📐 Site Characteristics</h3>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="required-section">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        fl_terrace = st.checkbox("🌿 Terrace")
        terrace_sqm = st.number_input("Terrace Area (sqm, approx.)", min_value=0, max_value=4000, value=8) if fl_terrace else 0
        fl_garden = st.checkbox("🌳 Garden")
        garden_sqm = st.number_input("Garden Area (sqm, approx.)", min_value=0, max_value=200000, value=50) if fl_garden else 0

    with col2:
        fl_floodzone = st.checkbox("🌊 Flood Zone")
        heating_type_list = ["Solar", "Electric", "Gas", "Pellet", "FuelOil", "Wood", "Carbon", "MISSING"]
        heating_type = st.selectbox("🌡️ Heating Type", heating_type_list)

    st.markdown("</div>", unsafe_allow_html=True)

# --- PREDICTION BUTTON & PRICE ---
col_btn, col_price = st.columns([1,2])
with col_btn:
    predict_btn = st.button("Predict Price")
with col_price:
    price_placeholder = st.empty()

# --- COLLECT INPUTS & PREDICTION ---
equipped_kitchen_label = equipped_kitchen_map.get(equipped_kitchen, "UNKNOWN")
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
    "fl_double_glazing": fl_double_glazing,
    "equipped_kitchen": equipped_kitchen_label,
    "state_building": state_building,
    "heating_type": heating_type,
    "fl_floodzone": fl_floodzone,
    "zip_code": zip_code,
}

if predict_btn:
    epc_to_energy = {"A+":50,"A":75,"B":100,"C":150,"D":200,"E":250,"F":300,"G":400,"Unknown":150}
    input_data["primary_energy_consumption_sqm"] = epc_to_energy.get(epc_rating, 150)
    try:
        predicted_price = predict(input_data)
        price_placeholder.markdown(f"""
            <div style="padding:15px;border-radius:1px">
                <h3>💶 Estimated Property Price: €{predicted_price:,.2f}</h3>
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        price_placeholder.error(f"Prediction failed: {e}")

st.markdown("""
    <hr>
    <p style="text-align:center; color:#666; font-size:13px;">
        © 2025 Immo Eliza — All rights reserved
    </p>
""", unsafe_allow_html=True)