import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import ast

# Suppress the deprecation warning
st.set_option('deprecation.showPyplotGlobalUse', False)


st.set_page_config(page_title="Plotting Demo")

st.title('Analytics')

# Load the data
new_df = pd.read_csv('datasets/data_viz1.csv')
feature_text = pickle.load(open('datasets/feature_text.pkl', 'rb'))

# Load the unique sectors data
unique_sectors = pickle.load(open('datasets/unique_sectors.pkl', 'rb'))

# Load the wordcloud DataFrame data
wordcloud_df = pd.read_pickle('datasets/wordcloud_df.pkl')


# Select numeric columns for aggregation
numeric_cols = ['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']
group_df = new_df.groupby('sector')[numeric_cols].mean()

# Sector Price per Sqft Geomap
st.header('Sector Price per Sqft Geomap')
fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                        color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                        mapbox_style="open-street-map", width=1200, height=700, hover_name=group_df.index)
st.plotly_chart(fig, use_container_width=True)

# Display the header
st.header('Features Wordcloud')

# Sidebar with the sector dropdown
selected_sector = st.selectbox('Select Sector:', ['overall'] + wordcloud_df['sector'].unique().tolist())

# Check if the selected sector is 'overall'
if selected_sector == 'overall':
    # Combine all features for all sectors into a single list (main)
    main = [item for sublist in wordcloud_df['features'].dropna().apply(ast.literal_eval) for item in sublist]
    # Convert the list to a string for WordCloud
    filtered_text = ' '.join(main)
else:
    # Filter the wordcloud_df based on the selected sector
    filtered_text = ' '.join(wordcloud_df.loc[wordcloud_df['sector'] == selected_sector, 'features'].dropna())

# Check if there are non-empty values in filtered_text before generating WordCloud
if filtered_text:
    # Generate and display the WordCloud
    wordcloud = WordCloud(width=800, height=800, background_color='black', stopwords=set(['s']),
                          min_font_size=10).generate(filtered_text)

    fig, ax = plt.subplots(figsize=(8, 8), facecolor=None)
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot(fig)
else:
    # Inform the user that there are no features for the selected sector
    st.warning(f"No features available for the selected sector: {selected_sector}")


# Area Vs Price
st.header('Area Vs Price')

# Dropdown for property type
property_type = st.selectbox('Select Property Type', ['flat', 'house'], key='property_type')

# Dropdown for sector with an overall option
selected_sector = st.selectbox('Select Sector', ['overall'] + new_df['sector'].unique().tolist(), key='selected_sector')

if selected_sector == 'overall':
    # Create an overall view for all sectors
    fig1 = px.scatter(new_df[new_df['property_type'] == property_type], x="built_up_area", y="price",
                      color="bedRoom", size="price_per_sqft", title="Area Vs Price - Overall")
else:
    # Filter data based on selected sector
    filtered_df = new_df[(new_df['property_type'] == property_type) & (new_df['sector'] == selected_sector)]

    if property_type == 'house':
        fig1 = px.scatter(filtered_df[filtered_df['property_type'] == 'house'], x="built_up_area", y="price",
                          color="bedRoom", size="price_per_sqft", title=f"Area Vs Price - {selected_sector}")
    else:
        fig1 = px.scatter(filtered_df[filtered_df['property_type'] == 'flat'], x="built_up_area", y="price",
                          color="bedRoom", size="price_per_sqft", title=f"Area Vs Price - {selected_sector}")

# Plotly chart
st.plotly_chart(fig1, use_container_width=True)

# Adding tooltip to see additional information like bedroom, price, area
fig1.update_traces(hovertemplate='<b>Price:</b> %{y:$,.0f}<br><b>Area:</b> %{x:.2f} sqft<br><b>Bedrooms:</b> %{marker.color}')

# BHK Pie Chart
st.header('BHK Pie Chart')
sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0, 'overall')
selected_sector = st.selectbox('Select Sector', sector_options)
if selected_sector == 'overall':
    fig2 = px.pie(new_df, names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)
else:
    fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)



# Side by Side BHK price comparison
st.header('Side by Side BHK Price Comparison')

# Dropdown for selecting the sector
selected_sector_boxplot = st.selectbox('Select Sector:', ['Overall'] + new_df['sector'].unique().tolist())

# Filter the data based on the selected sector
if selected_sector_boxplot == 'Overall':
    filtered_df_boxplot = new_df[new_df['bedRoom'] <= 4]
else:
    filtered_df_boxplot = new_df[(new_df['bedRoom'] <= 4) & (new_df['sector'] == selected_sector_boxplot)]

# Create the boxplot
fig3 = px.box(filtered_df_boxplot, x='bedRoom', y='price', title='BHK Price Range')

# Display the boxplot
st.plotly_chart(fig3, use_container_width=True)

st.header('Histogram for Property Type (Price Range)')

# Dropdown for selecting the sector
selected_sector_histogram = st.selectbox('Select Sector:', ['Overall'] + new_df['sector'].unique().tolist(), key='select_sector_histogram')

# Filter the data based on the selected sector
if selected_sector_histogram == 'Overall':
    filtered_df_histogram = new_df
else:
    filtered_df_histogram = new_df[new_df['sector'] == selected_sector_histogram]

# Create the histogram
fig4 = px.histogram(filtered_df_histogram, x='price', color='property_type', marginal='rug', title='Price Range Distribution by Property Type')

# Display the histogram
st.plotly_chart(fig4, use_container_width=True)


# Side by Side Distplot for property type
st.header('Side-by-Side Distribution Plot for Property Type (Price Range)')

# Dropdown for selecting the sector
selected_sector_distplot = st.selectbox(
    'Select Sector:',
    ['Overall'] + new_df['sector'].unique().tolist(),
    key='select_sector_distplot'
)

# Filter the data based on the selected sector
if selected_sector_distplot == 'Overall':
    filtered_df_distplot = new_df
else:
    filtered_df_distplot = new_df[new_df['sector'] == selected_sector_distplot]

# Create the distribution plot
fig5, ax = plt.subplots(figsize=(10, 6))
for property_type in filtered_df_distplot['property_type'].unique():
    sns.kdeplot(
        filtered_df_distplot[filtered_df_distplot['property_type'] == property_type]['price'],
        ax=ax,
        label=property_type,
        fill=False
    )

ax.set_title('Price Range Distribution by Property Type')
ax.set_xlabel('Price')
ax.set_ylabel('Density')
ax.legend()

# Display the distribution plot
st.pyplot(fig5)

#Visualizing Gurgaon Sectors on Map
import folium
from folium import plugins
from streamlit_folium import folium_static

st.header('Visualizing Gurgaon Sectors on Map')

# Set the center coordinates for Gurgaon
gurgaon_center = [28.4595, 77.0266]

# Create a Folium map centered around Gurgaon
m = folium.Map(location=gurgaon_center, zoom_start=13)

# Add title
title_html = '''
<h3 align="center" style="font-size:20px"><b>Gurgaon Sectors Map</b></h3>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Add custom marker icon
marker_icon = folium.CustomIcon(
    icon_image='https://imageurl.com/custom_marker_icon.png',
    icon_size=(30, 30),
    icon_anchor=(15, 30),
)

# Add markers for each sector with custom icon
for index, row in new_df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['sector'],
        icon=marker_icon
    ).add_to(m)

# Beautify the map with plugins (optional)
plugins.Fullscreen(position='topright', force_separate_button=True).add_to(m)
plugins.MousePosition().add_to(m)
plugins.MiniMap(toggle_display=True).add_to(m)

# Display the map
folium_static(m)

#FurnishingTypeAnalysis
st.header('Furnishing Type Analysis')

# Dropdown for selecting the sector
selected_sector_furnishing = st.selectbox(
    'Select Sector:',
    ['Overall'] + new_df['sector'].unique().tolist(),
    key='furnishing_sector'
)

# Filter the data based on the selected sector
if selected_sector_furnishing == 'Overall':
    filtered_df_furnishing = new_df
else:
    filtered_df_furnishing = new_df[new_df['sector'] == selected_sector_furnishing]

# Map furnishing type codes to labels
furnishing_labels = {0: 'Unfurnished', 1: 'Semi-Furnished', 2: 'Furnished'}
filtered_df_furnishing['furnishing_label'] = filtered_df_furnishing['furnishing_type'].map(furnishing_labels)

# Concatenate numerical code and label for display
filtered_df_furnishing['display_label'] = (
    filtered_df_furnishing['furnishing_type'].astype(str) + '-' + filtered_df_furnishing['furnishing_label']
)

# Create the pie chart
fig_furnishing_streamlit = px.pie(
    filtered_df_furnishing,
    names='display_label',
    title=f'Furnishing Type Distribution in {selected_sector_furnishing} Sector',
    labels={'display_label': 'Furnishing Type'},
)

# Display the pie chart
st.plotly_chart(fig_furnishing_streamlit, use_container_width=True)