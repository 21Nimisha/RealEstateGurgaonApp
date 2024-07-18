import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Set page configuration with background color and layout
st.set_page_config(
    page_title="Real Estate Price Prediction",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data and pipeline
with open('df.pkl', 'rb') as file:
    df = pickle.load(file)

with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Page header with background color
st.markdown(
    """
    <style>
    body {
        background-color: #000000; /* Black background */
        color: #FFFFFF; /* White text color */
        padding: 10px; /* Add padding for the border effect */
    }
    </style>
    """,
    unsafe_allow_html=True
)
#st.dataframe(df)
# Main content
st.header('Enter your inputs')

# Property type
property_type = st.selectbox('Property Type', ['flat', 'house'])

# Sector
sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))

# Bedrooms
bedrooms = float(st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist())))

# Bathrooms
bathroom = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist())))

# Balconies
balcony = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))

# Property age
property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

# Built-up area
built_up_area = float(st.number_input('Built-Up Area'))

# Servant room
servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))

# Store room
store_room = float(st.selectbox('Store Room', [0.0, 1.0]))

# Furnishing type
furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))

# Luxury category
luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))

# Floor category
floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

# Prediction button
if st.button('Predict'):
    # Format data as DataFrame
    data = [[property_type, sector, bedrooms, bathroom, balcony, property_age, built_up_area,
             servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony', 'agePossession',
               'built_up_area', 'servant room', 'store room', 'furnishing_type', 'luxury_category', 'floor_category']

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)

    # Predict
    base_price = np.expm1(model.predict(one_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22

    # Display result
    st.markdown(f"**The price of the flat is between {round(low, 2)} Cr and {round(high, 2)} Cr**")
