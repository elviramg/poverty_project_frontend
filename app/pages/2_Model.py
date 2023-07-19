import streamlit as st
import pandas as pd
import json
import geopandas as gpd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('data/Labor_Poverty.csv')

# Add title and header
st.title("Labor Poverty in Mexico")

# Dropdown for selecting a date
date = st.selectbox('Select a date:', df['Unnamed: 0'].unique())

# Filter the dataset based on the selected date
selected_data = df[df['Unnamed: 0'] == date].transpose().reset_index()
selected_data.columns = ['State', 'Poverty Rate']
selected_data = selected_data.iloc[1:]  # Exclude the date row
selected_data.set_index("State", inplace=True)

# Load GeoJSON file
with open("data/mexicoHigh.json") as response:
    geo = json.load(response)

# Convert GeoJSON to GeoDataFrame
gdf = gpd.GeoDataFrame.from_features((geo))

# Merge GeoDataFrame with selected data
merged = gdf.join(selected_data.astype(float))

# Plotting
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
merged.plot(column='Poverty Rate', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
plt.title(f'Poverty Rate by State in Mexico for {date}')

# Display on Streamlit
st.pyplot(fig)
