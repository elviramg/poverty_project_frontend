import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import geopandas as gpd
#from app.utils import get_csv, get_recovery_graph
from dateutil.relativedelta import relativedelta
import altair as alt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import matplotlib.colors as mcolors
from datetime import datetime

def get_csv():
    labor_pov = pd.read_csv("data/Labor_Poverty.csv", index_col=0, parse_dates=True)
    labor_pov = labor_pov.replace({"ND": None})
    labor_pov = labor_pov.astype(float)

    # Dictionary to map Spanish month abbreviations to English abbreviations
    spanish_to_english_months = {
        "ene": "01",
        "feb": "02",
        "mar": "03",
        "abr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "ago": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dic": "12",
    }

    # Convert month abbreviations to the desired format "Jan-05", "Feb-05", etc.
    new_index = [spanish_to_english_months[month[:3]] + "-" + month[-2:] for month in labor_pov.index]
    labor_pov.index = pd.to_datetime(new_index, format="%m-%y")

    return labor_pov

def get_model_csv():
    model_pred = pd.read_csv("output/model_prediction.csv", index_col=0).transpose()
    new_index = list(model_pred.index)
    model_pred.index = pd.to_datetime(new_index, format="%m-%Y")
    return model_pred

def yearly_rankings(data, start_year=2005, end_year=2023):
    """"THIS FUNCTION RETURNS A DATAFRAME WITH THE YEARLY RANKINGS OF POVERTY BY STATE (% OF PEOPLE IN LABOR POVERTY)
    OVER A SELECTED RANGE OF YEARS (FIRST PLACE HAS HIGHEST RATE, LAST PLACE HAS LOWEST.)"""
    rank_df = None
    years = [i for i in range(start_year, end_year + 1)]
    df_start = (start_year - 2005) * 4
    df_end = (end_year - 2005) * 4
    if 2023 in years:
        df_end = 72
    start = df_start
    for i in range((df_end - df_start) // 4 + 1):
        end = start + 4
        batch = data.iloc[start:end,:].mean().sort_values()
        rank_series = pd.Series([i + 1 for i in range(len(batch))], index=batch.index).sort_index()
        if rank_df is None:
            rank_df = pd.DataFrame(rank_series).T
        else:
            rank_df.loc[i] = rank_series.to_dict().values()
        start += 4
        if end >= 72:
            break
    if 2023 in years:
        batch_2023 = data.iloc[df_end,:].sort_values(ascending=False)
        rank_2023 = pd.Series([i + 1 for i in range(len(batch_2023))], index=batch_2023.index).sort_index()
        rank_df.loc[len(rank_df)] = rank_2023.to_dict().values()
    rank_df.index = years
    return rank_df

def get_recovery_graph(recovered_df):
    state_recovery_data = recovered_df.sort_values('Months since 2020-04-01')

    # Crear lista de colores basada en los valores del DataFrame
    colors = []
    max_value = state_recovery_data['Months since 2020-04-01'].max()
    for value in state_recovery_data['Months since 2020-04-01']:
        if value == -1:
            colors.append('red')
        else:
            # Genera un valor de color basado en el valor actual
            color_intensity = 1 - np.clip(value / max_value, 0, 1)  # Esto asegura que el verde no sea demasiado oscuro
            colors.append(mcolors.to_rgba((1 - color_intensity, 1, 0)))  # Establece un color en formato RGB

    fig, ax = plt.subplots(figsize=(12, 10))
    state_recovery_data['Months since 2020-04-01'].plot(kind='barh', ax=ax, color=colors, edgecolor='black', legend=False)
    ax.set_title('States recovery time from April 2020', fontsize=16)
    ax.set_xlabel('Months since Abril 2020', fontsize=14)
    ax.set_ylabel('Months from April 2020', fontsize=14)
    ax.text(0.5, 0.09, 'A shorter green bar indicates faster return to pre-COVID poverty levels.', transform=ax.transAxes, fontsize=15, va='top')
    ax.axvline(0, color='red', linestyle='--')

    return fig

data = get_csv()

st.set_page_config(layout="wide")

#adding marging specs for the main page with css inyection
margins_css = """
    <style>
        .main > div {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
            padding-top: 0.5rem;
        }
    </style>
"""

st.markdown(margins_css, unsafe_allow_html=True)

st.title("Poverty Across Mexico")
st.markdown("### " + ("Today 37.7% of Mexico's population lives in Labor Poverty."))
st.markdown("Here you will find interactive DataViz tools to expand on some insights. Feel free to explore and play around")

col1, col2 = st.columns([1,1])

with col1:

    st.markdown(("## " + ("Labor Poverty by State")))
    st.markdown("Explore the percentage of people living in poverty for different states across Mexico over time. \n Use the multiselect widget to select one or more states for comparison.")

    def line_plots(data: pd.DataFrame):
        """Renders line plots for selected regions (states) from data argument."""

        # Get the state names (column names) from the DataFrame
        states_options = data.columns.tolist()

        # Allow the user to select one or more states using a multiselect widget
        states = st.multiselect(
            label="States",
            options=states_options,
            default=["National"],
        )

        # Filter data for the selected states
        selected_states = data[states]

        if selected_states.empty:
            st.warning("No state selected!")
        else:
            # Create a DataFrame for the selected states and reset the index
            selected_states_df = selected_states.reset_index()

            # Convert the datetime values in the index to strings
            selected_states_df["index"] = selected_states_df["index"].dt.strftime("%Y-%m-%d")

            # Melt the DataFrame to make it suitable for Altair
            selected_states_melted = pd.melt(selected_states_df, id_vars="index", var_name="State", value_name="Percentage")

            # Create the Altair chart
            chart = alt.Chart(selected_states_melted).mark_line().encode(
                x=alt.X("index:T", title="Date"),
                y=alt.Y("Percentage:Q", title="Percentage"),
                color=alt.Color("State:N", title="State", scale=alt.Scale(scheme="category10")),
                tooltip=["index:T", "Percentage:Q", "State:N"]
            ).properties(
                width=550,
                height=400
            ).configure_axis(
                labelColor="white",
                titleColor="white"
            ).configure_legend(
                labelColor="white",
                titleColor="white"
            ).configure_title(
                color="white"
            ).interactive()

        # Display the Altair chart using Streamlit's altair_chart function
        st.altair_chart(chart)

    # Call the function with the 'data' DataFrame as the argument
    data = get_csv()
    line_plots(data)

with col2:

    st.markdown("## Poverty Rate by State in Mexico")
    st.markdown("Visualize the poverty rate across different states in Mexico for a specific date. \n Use the dropdown menu to choose a date.")

    # Function to load data
    @st.cache
    def load_data():
        return pd.read_csv('data/Labor_Poverty.csv')

    # Function to load GeoJSON
    @st.cache
    def load_geojson():
        with open("data/mexicoHigh.json", "r") as file:
            return json.load(file)

    # Load the dataset
    df = load_data()

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
    fig, ax = plt.subplots(1, 1, figsize=(10, 50))

    # 1. Hacer el fondo de los ejes y de la figura transparente
    ax.set_facecolor("none")
    fig.patch.set_alpha(0.0)
    ax.axis('off')  # Desactiva los ejes para que no se muestren

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)

    # 2. Cambiar el color de borde a blanco
    merged.plot(column='Poverty Rate', cmap='YlOrRd', linewidth=1, ax=ax, edgecolor='black', legend=True, cax=cax)

    # 3. Cambiar el color de los textos y las etiquetas de los ejes a blanco
    ax.tick_params(axis='both', colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.set_title(f'Data for {date}', color='white', fontsize=18)


    # 4. Ajustar el color del texto en la barra de colores a blanco
    cax.tick_params(color='white')
    cax.xaxis.label.set_color('white')
    cax.yaxis.label.set_color('white')
    for label in cax.yaxis.get_ticklabels():
        label.set_color("white")

    # Display on Streamlit
    st.pyplot(fig)


def main():
    st.markdown(("## " + ("Recovery from Labor Poverty Post-COVID")))
    st.markdown(
        (
            "Explore which states have recovered from labor poverty since the COVID pandemic hit Mexico. The data shows the number of months each state took to return to pre-pandemic poverty levels"
            "\n a (-)1 indicates the state has not recover from the pandemic i.e The current percentage in population living in labor poverty is higher than that of April 2020."
        )
    )

    july_index = data.index.get_loc('2020-07-01')
    july_index = data.index.get_loc('2020-07-01')
    states_list = data.columns

    states_past_covid = []
    for state in states_list:
        pre_cov_pov = data[state].loc['2020-01-01']
        states_past_covid.append(data[july_index:][state][data[state][july_index:] <= pre_cov_pov].sort_index().head(1))

    df_months_recovered = pd.DataFrame(states_past_covid)

    # Fill NaN values with -1
    df_months_recovered = df_months_recovered.fillna(-1)

    # Quarter for COVID over which we measure recovery time
    april_2020 = pd.Timestamp('2020-04-01')

    # Initialize Dict that will creat recovery df
    recovered_dictionary = {}

    for state in states_list:
        # Create Boolean Mask for Final Recovery Data Frame
        mask = df_months_recovered.loc[state] != -1

        if mask.any():
            first_non_nan_date = df_months_recovered.loc[state][df_months_recovered.loc[state] != -1].index[0]
            diff = relativedelta(first_non_nan_date, april_2020)
            months_diff = diff.years * 12 + diff.months
            recovered_dictionary[state] = months_diff
        else:
            recovered_dictionary[state] = -1

    recovered_df = pd.DataFrame(recovered_dictionary.values(), index = recovered_dictionary.keys())
    recovered_df.rename(columns = {0:'Months since 2020-04-01'},inplace = True)
    recovered_df = recovered_df.sort_values('Months since 2020-04-01', ascending = False)
    #recovered_df.value_counts().sort_index()

    graph = get_recovery_graph(recovered_df)
    graph.set_size_inches(20, 15)
    st.pyplot(graph)

    st.write("""As we can see 13 States had not recovered to pre-pandemic poverty levels which are from Mexico City till Michoacán.
             Only 8 recovered within a year.  6 states required 1-2 years to recover.  5 took over 2 years.""")

if __name__ == '__main__':
    main()
