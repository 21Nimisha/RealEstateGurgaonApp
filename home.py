import streamlit as st
import pandas as pd
import pickle

# Set the page configuration
st.set_page_config(
    page_title="Gurgaon Real Estate Analytics App",
    page_icon="👋",
)

# Load the sample data
with open('df.pkl', 'rb') as file:
    df = pickle.load(file)

# Add home image
# Add home image
st.image("home.jpg", use_column_width=True)

# Page Title
st.markdown("<h1 style='color:#009688;'>Welcome to Gurgaon Real Estate Insight Hub!👋</h1>", unsafe_allow_html=True)


# Introduction
st.write("Welcome to the Real Estate Gurgaon App repository! This project aims to simplify property search in Gurgaon, India, using machine learning algorithms. Explore our modules designed to enhance your property buying experience. Analyze Gurgaon real estate data to make informed decisions about your next property investment.")

# Modules Overview
st.header('Modules Overview')

## Price Prediction Module
st.subheader('1. Price Prediction Module')
st.write("- Predicts property prices based on user-defined criteria (e.g., number of rooms, square footage, location preferences, floor level).")
st.write("- Provides tailored recommendations based on sector-specific data.")

## Analytics Module
st.subheader('2. Analytics Module')
st.write("- **Spatial Analysis**: Visualize Gurgaon sectors colored by property prices for informed decision-making.")
st.write("- **Price Distribution Across Sectors**: Box plots showing price variations across different sectors.")
st.write("- **Price Vs Square Foot Analysis**: Scatter plots to analyze price correlation with property square footage.")
st.write("- **Number of Rooms Pie Chart**: Insights into distribution of property sizes across Gurgaon sectors.")

## Recommendation System Module
st.subheader('3. Recommendation System Module')
st.write("- Recommends properties based on user preferences and similarity in amenities between different societies.")

# Data Overview
st.subheader("Data Overview:")
st.write("Our dataset includes information about various properties in Gurgaon, such as property name, price, area, and features.")
# Display Sample Data (first 5 to 10 rows)
#st.subheader("Sample Data:")
#st.dataframe(df.head(11))

# Pages Overview
st.subheader("Pages Overview:")
st.write("1. **Price Predictor App:** Predict the price range based on user-defined features. 📈")
st.write("2. **Analytics Module:** Analyze properties using geomaps, side-by-side comparisons, word clouds, and more. 🗺️")
st.write("3. **Recommendations App:** Get property recommendations based on location preferences. 🏡")

# Background Styling
st.markdown("<style>body{background-color:#f0f0f0;}</style>", unsafe_allow_html=True)

# How to Use the Data
st.subheader("How to Use the Data:")
st.write("1. Enter feature requirements in the Price Predictor App.")
st.write("2. Explore analytics and comparisons in the Analytics Module.")
st.write("3. Receive personalized property recommendations in the Recommendations App.")

# Sample Data Usage
st.subheader("Sample Data Usage:")
st.write("1. **User Input:** Features for a 3BHK flat.")
st.write("2. **Output:** Predicted price range, analytics, and top 5 similar apartments.")

# Sample Scenario
with st.expander("Sample Scenario"):
    st.write("Let's look at a sample scenario using the provided data.")
    st.write("1. User enters features for a 3BHK flat.")
    st.write("2. The system predicts the price range, provides analytics, and recommends the top 5 similar apartments.")

# Conclusion
st.subheader("Conclusion:")
st.write("Empower yourself with valuable insights to make informed decisions in the dynamic real estate market.")


# Display Sample Data
# Code Snippet
st.subheader("Code Snippet:")
st.code("""
# Sample code to load data
import pandas as pd
sample_data = pd.read_csv('your_sample_data.csv')
""")

# Button for Interaction
if st.button("Click me"):
    st.write("Button clicked!")
    # Display Sample Data
    st.subheader("Sample Data:")
    st.dataframe(df.head(10))
