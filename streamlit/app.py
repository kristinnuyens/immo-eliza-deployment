import streamlit as st
from predict import predict_price

def main():
    st.title("Property Price Prediction")
    
    # Input fields
    region = st.selectbox("Region", ['Flanders','Brussels-Capital','Wallonia'])
    province = st.selectbox("Province", ['Hainaut', 'East Flanders', 'West Flanders','Limburg','Brussels','Flemish Brabant',
                            'Walloon Brabant','Antwerp','Brussels','Liège','Luxembourg','Namur'])
    living_area = st.number_input("Living Area (sqm)", min_value=0)
    property_type = st.selectbox("Type of Property", ['APARTMENT', 'HOUSE'])
    subproperty_type = st.selectbox("Type of Sub-property", ['HOUSE','APARTMENT','VILLA','SERFVICE_FLAT'])
    bedrooms = st.number_input("Bedrooms", min_value=0)
    postal_code = st.number_input("Postal Code", min_value=0)
    





    # Optional inputs
    garden = st.checkbox("Garden")
    swimming_pool = st.checkbox("Swimming Pool")
    
    if st.button("Predict"):
        # Example input structure
        data = {
            "LivingArea": living_area,
            "TypeOfProperty": property_type,
            "Bedrooms": bedrooms,
            "PostalCode": postal_code,
            "Garden": garden,
            "SwimmingPool": swimming_pool
        }
        # Call the predict function and display the result
        prediction = predict_price(data)
        st.success(f"Predicted Price: {prediction}")

if __name__ == "__main__":
    main()