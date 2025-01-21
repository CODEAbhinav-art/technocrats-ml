import streamlit as st
import pandas as pd

st.title('machine learning app')
st.info('its an amazing ml app created from technocrats project')

with st.expander('Data'):
   st.write('**Raw data**')
   df=pd.read_csv('https://raw.githubusercontent.com/dataprofessor/palmer-penguins/refs/heads/master/data/penguins_cleaned.csv')
   df
