import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import geopandas as gpd
#from app.utils import get_csv, get_model_csv
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
data_model = get_model_csv()
merged_data = pd.concat([data, data_model])

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

st.markdown("<div align='center'>", unsafe_allow_html=True)

st.title("Poverty Across Mexico")
st.markdown("### " + ("Today 37.7% of Mexico's population lives in Labor Poverty."))
st.markdown("Here you will find interactive DataViz tools to expand on some insights. Feel free to explore and play around")

st.markdown(("## " + ("Labor Poverty by State")))
st.markdown(
    (
        "Explore the percentage of people living in poverty for different states across Mexico over time. \n Use the multiselect widget to select one or more states for comparison.\n --------"
    )
)

def line_plots(data: pd.DataFrame, data_model: pd.DataFrame):
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
    selected_states_dotted = data_model[states]
    if selected_states.empty:
        st.warning("No state selected!")
    else:
        # Create a DataFrame for the selected states and reset the index
        selected_states_df = selected_states.reset_index()
        selected_states_df_dotted = selected_states_dotted.reset_index()
        # Convert the datetime values in the index to strings
        selected_states_df["index"] = selected_states_df["index"].dt.strftime("%Y-%m-%d")
        selected_states_df_dotted["index"] = selected_states_df_dotted["index"].dt.strftime("%Y-%m-%d")
        # Melt the DataFrame to make it suitable for Altair
        selected_states_melted = pd.melt(selected_states_df, id_vars="index", var_name="State", value_name="Percentage")
        selected_states_melted_dotted = pd.melt(selected_states_df_dotted, id_vars="index", var_name="State", value_name="Percentage")
        # Create the Altair chart without configurations
        chart = alt.Chart(selected_states_melted).mark_line().encode(
            x=alt.X("index:T", title="Date"),
            y=alt.Y("Percentage:Q", title="Percentage"),
            color=alt.Color("State:N", title="State", scale=alt.Scale(scheme="category10")),
            tooltip=["index:T", "Percentage:Q", "State:N"]
        ).properties(
            width=550,
            height=400
        )
        # Create Dotted data without configurations
        chart_dotted = alt.Chart(selected_states_melted_dotted).mark_line(strokeDash=[5, 5]).encode(
            x=alt.X("index:T"),
            y=alt.Y("Percentage:Q"),
            color=alt.Color("State:N", scale=alt.Scale(scheme="category10")),
            tooltip=["index:T", "Percentage:Q", "State:N"]
        )
        # Combine both charts and then add configurations
        combined_chart = alt.layer(chart, chart_dotted).properties(
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
        # Use a container to center the Altair chart in Streamlit
        with st.container():
            # Add CSS to center the chart
            st.markdown("""
                <style>
                    .container {
                        display: flex;
                        justify-content: center;
                    }
                </style>
            """, unsafe_allow_html=True)
            # Display the Altair chart inside the container
            st.altair_chart(combined_chart)
# Call the function with the 'data' DataFrame as the argument
data = get_csv()
data_model = get_model_csv()
line_plots(data, data_model)
