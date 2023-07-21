import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import get_csv
from gettext import NullTranslations

data = get_csv()

st.markdown(("## " + ("Poverty Across Mexico")))

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
        for state in selected_states.columns:
            plt.plot(selected_states.index, selected_states[state], label=state)

        plt.xlabel("Date")
        plt.ylabel("Y")  # Replace with appropriate Y-axis label
        plt.title("Title")
        plt.legend()
        st.pyplot()  # Display the plot using Streamlit's pyplot function

# Call the function with the 'data' DataFrame as the argument
data = get_csv()
line_plots(data)
