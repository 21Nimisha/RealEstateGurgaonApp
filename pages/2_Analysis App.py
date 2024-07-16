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
st.header('Side by Side Distplot for property type')
fig4 = plt.figure(figsize=(10, 4))
sns.histplot(new_df[new_df['property_type'] == 'house']['price'], label='house', kde=True)
sns.histplot(new_df[new_df['property_type'] == 'flat']['price'], label='flat', kde=True)
plt.legend()
st.pyplot(fig4)
