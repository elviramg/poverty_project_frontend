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
        Poverty poses a significant challenge to Mexico. According to the latest data from CONEVAL (National Council for the Evaluation of Social Development Policy), nearly 40% of the country’s population lives in some form of poverty ([CONEVAL, 2022](https://www.coneval.org.mx/SalaPrensa/Comunicadosprensa/Documents/2022/COMUNICADO_18_ITLP_3T_2022.pdf)).\n
        Hence, identifying areas at risk of increasing poverty may prove helpful for policymakers to take effective steps towards tackling and preventing such increases. \n
        This might translate into a better allocation of human and economic resources or selective monitoring of poverty indicators in vulnerable states.
""")

with col2:
    st.markdown("""
    Our data comes from CONEVAL’s Labor Poverty Trend Index (ITLP by its Spanish acronym). Our main goal is to understand how labor poverty has evolved over time through statistical analysis derived from the data gathered, as well as to provide a benchmark view into future trends utilizing elementary data engineering techniques. \n With this project we seek to develop our skills in data analysis by providing policy makers and community leaders with a resource for making data-driven decisions to better the people of Mexico.
    We also aim to contribute to further advancement of social research in Mexico and help government officials and institutions implement comprehensive social and economic policies where needed most. \n
    For full transparency, you can find the public data used for this project [here](https://www.coneval.org.mx/Medicion/Paginas/ITLP-IS_pobreza_laboral.aspx).
    """)

st.image("pob_ingreso_menor_canasta.png", caption="Percentage of the population with labor income lower than the cost of the basic food basket", use_column_width=True)
