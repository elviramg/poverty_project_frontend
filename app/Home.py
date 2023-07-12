import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Website introduction/information
st.markdown ("""
             # Header
             ## Subheader
             Normal Text""")

# Upload DataFrame
df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)),'data','indicadores de pobreza municipal_2010.csv'), encoding='latin-1')

X = df['poblacion']
y = df['pobreza_pob']

fig, ax = plt.subplots()
ax.hist(X, bins=20)

st.pyplot(fig)
