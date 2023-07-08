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
df = pd.read_csv('indicadores de pobreza municipal_2010.csv')

X = df['total_population']
y = df['poverty_percentage']

plt.plot(X,y)
