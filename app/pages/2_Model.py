import streamlit as st
import pandas as pd
import json
import geopandas as gpd
import matplotlib.pyplot as plt

# Function to load data
@st.cache
def load_data():
    return pd.read_csv('data/Labor_Poverty.csv')

# Function to load GeoJSON
@st.cache
def load_geojson():
    with open("data/mexicoHigh.json", "r") as file:
        return json.load(file)

def main():
    # Load the dataset
    df = load_data()

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
    geo = load_geojson()

    # Convert GeoJSON to GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(geo)

    # Merge GeoDataFrame with selected data
    merged = gdf.set_index("name").join(selected_data.astype(float))

    # Plotting
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    merged.plot(column='Poverty Rate', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
    plt.title(f'Poverty Rate by State in Mexico for {date}')

    # Display on Streamlit
    st.pyplot(fig)

if __name__ == '__main__':
    main()
