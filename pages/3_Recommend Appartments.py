import streamlit as st
import pickle
import pandas as pd

# Load data
location_df = pickle.load(open('datasets/location_distance.pkl', 'rb'))
cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl', 'rb'))
cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))
cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl', 'rb'))

# Function to recommend properties with scores
def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'Property Name': top_properties,
        'Similarity Score': top_scores
    })

    return recommendations_df

# Streamlit app
st.set_page_config(page_title="Recommend Apartments", layout="wide")

# Title for the location and radius selection with color, bold, and background color
st.title('**Select Location and Radius**')
st.markdown('<style>h1{color:#4285f4;background-color:#f0f0f0;}</style>', unsafe_allow_html=True)

# Dropdown for selecting location
selected_location = st.selectbox('**Location**', sorted(location_df.columns.to_list()))

# Numeric input for selecting radius
radius = st.number_input('**Radius in kms**')

# Button to trigger the location-based search
if st.button('**Search by Location**'):
    result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()

    # Display search results with color, bold, and background color
    st.markdown(f"**Search Results:**")

    # Convert values from meters to kilometers
    result_ser_km = result_ser / 1000

    for key, value in result_ser_km.items():
        st.text(str(key) + " " + str(round(value, 2)) + ' km')

    # Display the result in a dataframe
    st.dataframe(result_ser_km)

# Title for the recommendation section with color, bold, and background color
st.title('**Recommend Apartments**')
st.markdown('<style>h1{color:#4285f4;background-color:#f0f0f0;}</style>', unsafe_allow_html=True)

# Dropdown for selecting an apartment
selected_apartment = st.selectbox('**Select an Apartment**', sorted(location_df.index.to_list()))

# Button to trigger the recommendations
if st.button('**Recommend**'):
    recommendation_df = recommend_properties_with_scores(selected_apartment)

    # Display recommendations in a formatted way with color, bold, and background color
    st.subheader('**Top Recommendations:**')

    # Apply CSS styling for the DataFrame
    css = """
    <style>
    .dataframe th {
        font-weight: bold;
        border: 1px solid #3498db;
        padding: 8px;
        text-align: left;
        background-color: #3498db;
        color: #ffffff;
    }
    .dataframe td {
        font-weight: bold;
        border: 1px solid #3498db;
        padding: 8px;
        text-align: left;
    }
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)

    # Display the result DataFrame
    st.dataframe(recommendation_df)
