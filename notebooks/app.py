import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Create tabs
tabs = ["Tab 1", "Tab 2", "Tab 3"]
active_tab = st.sidebar.radio("Select Tab", tabs)

# Tab 1
if active_tab == "Tab 1":
    st.title("Tab 1 Content")


# Tab 2
elif active_tab == "Tab 2":
    st.title("Tab 2 Content")


# Tab 3
elif active_tab == "Tab 3":
    st.title("Tab 3 Content")


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
