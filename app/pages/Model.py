import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import geopandas as gpd
from app.utils import get_csv, get_model_csv
from dateutil.relativedelta import relativedelta
import altair as alt
from mpl_toolkits.axes_grid1 import make_axes_locatable

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
