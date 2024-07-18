# Recommendations App

## Overview
The Gurgaon Real Estate Recommendation App is designed to assist property seekers in finding suitable properties in Gurgaon based on location preferences and similarity scores. The app leverages advanced machine learning techniques to provide personalized recommendations and a user-friendly interface to explore property options effectively.

## Key Features
1. **Location-Based Search:**
   - Property seekers can select a location and a radius to find properties within the specified distance.
   - The app displays properties within the chosen radius, helping explorers focus on specific areas of interest.

2. **Property Recommendations:**
   - Property seekers can select a specific property to receive recommendations for similar properties.
   - The app calculates similarity scores using a combination of three cosine similarity matrices, providing accurate and relevant suggestions.
   - Recommended properties are displayed along with their similarity scores, making it easy for explorers to compare options.

## How It Works
1. **Data Loading:**
   - The app loads precomputed cosine similarity matrices and a location-distance DataFrame.
   - These data files are essential for calculating similarity scores and performing location-based searches.

2. **Location Search:**
   - Explorers input a location and a search radius.
   - The app filters properties within the specified radius and displays them with their respective distances.

3. **Property Recommendations:**
   - Property seekers select a property to get recommendations.
   - The app combines multiple similarity matrices to compute overall similarity scores.
   - Top similar properties are displayed with their names and scores.

## User Interface
- **Location and Radius Selection:**
  - Dropdown for selecting the location.
  - Numeric input for specifying the radius in kilometers.
  - Button to trigger the search.

- **Property Recommendations:**
  - Dropdown for selecting an apartment.
  - Button to get recommendations.
  - Table displaying the top recommended properties and their similarity scores.

## Benefits
- **Personalized Recommendations:**
  - The app provides tailored property suggestions based on explorer input and similarity calculations.
  
- **Ease of Use:**
  - Intuitive interface for selecting locations, entering search parameters, and viewing results.
  
- **Data-Driven Insights:**
  - Recommendations are based on robust data analysis, ensuring accuracy and relevance.

## Deployment
- Ensure all dependencies are listed in the `requirements.txt` file.
- Deploy the app on Streamlit Cloud or any other hosting service that supports Python and Streamlit.
