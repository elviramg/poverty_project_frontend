import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Website introduction/information
st.markdown ("""
             # Header
             ## Subheader
             Normal Text""")


# Upload DataFrame
df = pd.read_csv('data/indicadores de pobreza municipal_2010.csv', encoding='latin-1')

X = df['poblacion']
y = df['pobreza_pob']

fig, ax = plt.subplots()
ax.hist(X, bins=20)

st.pyplot(fig)
