# Real Estate Price Prediction

## Overview
The Real Estate Price Prediction App estimates property prices in Gurgaon based on user-input features.
It utilizes a trained machine learning model to predict property prices, offering users an interactive interface to input property details and obtain price predictions.

##How to use

### 1. Input Selection:
- **Property Type:** Select the type of property (flat or house).
- **Sector:** Choose the sector in Gurgaon.
- **Bedrooms, Bathrooms, Balconies:** Select the number of each.
- **Property Age:** Age of the property.
- **Built-Up Area:** Enter the area in square feet.
- **Servant Room, Store Room:** Select if available.
- **Furnishing Type:** Choose from options available.
- **Luxury Category:** Specify the luxury level.
- **Floor Category:** Select the floor type.

### 2.Prediction:
- Click the "predict" button to see the estimated price range for the selected property based on the input features.

**Example**

**For example, if you select:**

- **Property Type:** Flat
- **Sector:** Sector 54
- **Bedrooms:** 3
- **Bathrooms:** 3
- **Built-Up Area:** 1800 sq ft
- ... (other inputs as per your interface)

Upon clicking "Predict," the app will display the estimated price range based on the model.

### User Interface

- **Property Details:**
- Dropdowns and input fields for selecting property features.
- Button to trigger the prediction.

- **Prediction Result:**
- Display of the estimated price range in crores.

## Deployment
- Ensure all necessary dependencies are listed in the requirements.txt file.
- Deploy the app on Streamlit CLoud or any other hosting service that supports Python and Streamlit.