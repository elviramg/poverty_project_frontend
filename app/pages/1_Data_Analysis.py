import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import geopandas as gpd
from utils import get_csv, get_recovery_graph
from dateutil.relativedelta import relativedelta

data = get_csv()

#adding marging specs for the main page with css inyection
margins_css = """
    <style>
        .main > div {
            padding-left: 2rem;
            padding-right: 2rem;
            padding-top: 0.5rem;
        }
    </style>
"""

st.markdown(margins_css, unsafe_allow_html=True)

st.markdown(("## " + ("Poverty Across Mexico")))

col1, col2 = st.columns([1,1])

with col1:
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
            # 1. Cambiar el tamaño de la figura a (15, 15)
            fig, ax = plt.subplots(figsize=(15, 15))

            for state in selected_states.columns:
                # Plot the data on the axes
                ax.plot(selected_states.index, selected_states[state], label=state)

            # 2. Hacer el fondo de los ejes y de la figura transparente
            ax.set_facecolor("none")
            fig.patch.set_alpha(0.0)

            # 3. Cambiar el color de los textos, las etiquetas de los ejes y las líneas de los ejes a blanco
            ax.tick_params(axis='both', colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')

            ax.set_xlabel("Date", color='white')
            ax.set_ylabel("Percentage", color='white')
            ax.set_title("Percentage of People Living in Poverty", color='white')

            # 4. Cambiar el color de los marcos de los ejes a blanco
            for spine in ax.spines.values():
                spine.set_edgecolor('white')

            ax.legend()

            # Display the plot using Streamlit's pyplot function
            st.pyplot(fig)

    # Call the function with the 'data' DataFrame as the argument
    data = get_csv()
    line_plots(data)


with col2:

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
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))

    # 1. Hacer el fondo de los ejes y de la figura transparente
    ax.set_facecolor("none")
    fig.patch.set_alpha(0.0)
    ax.axis('off')  # Desactiva los ejes para que no se muestren

    # 2. Cambiar el color de borde a blanco
    merged.plot(column='Poverty Rate', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='white', legend=True)

    # 3. Cambiar el color de los textos y las etiquetas de los ejes a blanco
    ax.tick_params(axis='both', colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    plt.title(f'Poverty Rate by State in Mexico for {date}', color='white', fontsize=18)

    # 4. Ajustar el color del texto en la barra de colores a blanco
    cax = plt.gcf().axes[-1]
    cax.tick_params(color='white')
    cax.xaxis.label.set_color('white')
    cax.yaxis.label.set_color('white')
    for label in cax.yaxis.get_ticklabels():
        label.set_color("white")

    # Display on Streamlit
    st.pyplot(fig)


def main():
    st.markdown(("## " + ("Which States haven't recovered from labor poverty since Covid?")))

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
    st.pyplot(graph)

    st.write("""As we can see 13 States had not recovered to pre-pandemic poverty levels which are from Mexico City till Michoacán.
             Only 8 recovered within a year.  6 states required 1-2 years to recover.  5 took over 2 years.""")

if __name__ == '__main__':
    main()
