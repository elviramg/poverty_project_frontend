import streamlit as st
import numpy as np
import pandas as pd

# Website introduction/information
st.markdown ("""
             # Header
             ## Subheader
             Normal Text""")


# Upload DataFrame
df = pd.read_csv('indicadores de pobreza municipal_2010.csv')
