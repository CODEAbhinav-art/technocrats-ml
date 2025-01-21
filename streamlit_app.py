import streamlit as st
import pandas as pd

st.title('ABHINAVs machine learning app😎')
st.info('My first ML project for_the TECHNOCRATS CLUB')

with st.expander('Data'):
   st.write('**Raw data**')
   df=pd.read_csv('https://raw.githubusercontent.com/dataprofessor/palmer-penguins/refs/heads/master/data/penguins_cleaned.csv')
   df
   st.write('**X**')
   X=df.drop('species',axis=1)
   X

   st.write('**y**')
   Y=df.species
   Y

with st.expander('Data Visualization'):
   st.scatter_chart(data=df,x='bill_length_mm',y='body_mass_g',color='species')

#Data preparations
with st.sidebar:
   st.header('Input features')
   island=st.selectbox('Island',('Biscoe','Dream','Torgersen'))
   bill_length_mm=st.slider('Bill length(mm)',32.1,59.6,43.9)
   bill_depth_mm=st.slider('Bill Depth(mm)',13.1,21.5,17.2)
   flipper_length_mm=st.slider('Flipper Length(mm)',172.0,231.0,201.0)
   body_mass_g=st.slider('Body Mass(gm)',2700.0,6300.0,4207.0)
   gender=st.selectbox('Gender',('Male','Female'))
   
# ddcde
#create a DAtaframe for the input features


