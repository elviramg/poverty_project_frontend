import streamlit as st
import pandas as pd
import pydeck as pdk

# Load the dataset
df = pd.read_csv('data/Labor_Poverty.csv')

# Dropdown for selecting a date
date = st.selectbox('Select a date:', df['Unnamed: 0'].unique())

# Filter the dataset based on the selected date
selected_data = df[df['Unnamed: 0'] == date].transpose().reset_index()
selected_data.columns = ['State', 'Poverty Rate']
selected_data = selected_data.iloc[1:]  # Exclude the date row

# Approximate latitude and longitude centroids for the states in Mexico
state_coords = {
    "Aguascalientes": {"latitude": 21.8853, "longitude": -102.2916},
    "Baja California": {"latitude": 30.8406, "longitude": -115.2838},
    "Baja California Sur": {"latitude": 26.0444, "longitude": -111.6661},
    "Campeche": {"latitude": 19.8301, "longitude": -90.5349},
    "Chiapas": {"latitude": 16.7569, "longitude": -93.1292},
    "Chihuahua": {"latitude": 28.6320, "longitude": -106.0691},
    "Coahuila de Zaragoza": {"latitude": 27.0587, "longitude": -101.7068},
    "Colima": {"latitude": 19.2452, "longitude": -103.7241},
    "Durango": {"latitude": 24.0277, "longitude": -104.6532},
    "Guanajuato": {"latitude": 21.0190, "longitude": -101.2574},
    "Guerrero": {"latitude": 17.4392, "longitude": -99.5451},
    "Hidalgo": {"latitude": 20.0911, "longitude": -98.7624},
    "Jalisco": {"latitude": 20.6595, "longitude": -103.3494},
    "México": {"latitude": 19.3548, "longitude": -99.6306},
    "Michoacán de Ocampo": {"latitude": 19.5665, "longitude": -101.7068},
    "Morelos": {"latitude": 18.6813, "longitude": -99.1013},
    "Nayarit": {"latitude": 21.7514, "longitude": -104.8455},
    "Nuevo León": {"latitude": 25.5922, "longitude": -99.9758},
    "Oaxaca": {"latitude": 17.0732, "longitude": -96.7266},
    "Puebla": {"latitude": 19.0414, "longitude": -98.2063},
    "Querétaro": {"latitude": 20.5888, "longitude": -100.3899},
    "Quintana Roo": {"latitude": 19.1817, "longitude": -88.4791},
    "San Luis Potosí": {"latitude": 22.1565, "longitude": -100.9855},
    "Sinaloa": {"latitude": 24.7903, "longitude": -107.3877},
    "Sonora": {"latitude": 29.2972, "longitude": -110.3309},
    "Tabasco": {"latitude": 17.8409, "longitude": -92.6189},
    "Tamaulipas": {"latitude": 24.2669, "longitude": -98.8363},
    "Tlaxcala": {"latitude": 19.3139, "longitude": -98.2404},
    "Veracruz de Ignacio de la Llave": {"latitude": 19.1809, "longitude": -96.1429},
    "Yucatán": {"latitude": 20.7099, "longitude": -89.0943},
    "Zacatecas": {"latitude": 22.7709, "longitude": -102.5832},
    "Ciudad de México": {"latitude": 19.4326, "longitude": -99.1332},
    "Sinaloa": {"latitude": 24.7903, "longitude": -107.3877},
}

# Map the coordinates to the selected_data DataFrame
selected_data['latitude'] = selected_data['State'].map(lambda x: state_coords.get(x, {}).get('latitude'))
selected_data['longitude'] = selected_data['State'].map(lambda x: state_coords.get(x, {}).get('longitude'))

get_fill_color='[255, (1-Poverty Rate/100)*255, (1-Poverty Rate/100)*255, 140]'

# Calculate the RGB values
selected_data['red'] = 255
selected_data['green'] = ((1 - selected_data['Poverty Rate'].astype(float)/100) * 255).astype(int)
selected_data['blue'] = selected_data['green']

# Visualize the data on a map
view_state = pdk.ViewState(latitude=23.6345, longitude=-102.5528, zoom=4)  # Centered around Mexico
layer = pdk.Layer('ScatterplotLayer', data=selected_data, get_position='[longitude, latitude]',
                  get_radius=50000, get_fill_color='[red, green, blue, 140]',
                  pickable=True)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
