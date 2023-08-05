import streamlit as st

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

st.markdown("""
             # 🇲🇽 Evolution of poverty in Mexico

             ## Predicting states at risk 📉

             ### Problem
            """)

col1, col2 = st.columns([1,1])

with col1:
    ## Poverty project Front
    st.markdown("""
        Poverty poses a significant challenge in the Country, according to CONEVAL's latest data, almost 40% of the country populations lives in poverty.\n
        So, identifying areas at risk of increasing poverty can help policymakers target interventions effectively. \n
        This intervention could lead to a better allocation of human and economic resources.
""")

with col2:
    st.markdown("""
    Our data comes from Coneval's Labor poverty Trend Index ('ITPL by its acronym in Spanish'). By sharing this information, our main goal it's to understand how labor poverty has evolved over time \n

    We seek to develop our skills in data analysis with a socially responsible approach towards our country.\n
    Hoping also that this can serve as an aid in the investigation of poverty and helping policymakers to combat it. \n
    To be transparent from the beginning, you can find the data for our project publicly available [here](https://www.coneval.org.mx/Medicion/Paginas/ITLP-IS_pobreza_laboral.aspx)
    """)

st.image("pob_ingreso_menor_canasta.png", caption="Percentage of the population with labor income lower than the cost of the food basket", use_column_width=True)
