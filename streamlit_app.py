import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

st.title('Machine Learning App by Abhinav😎')
st.info('My first ML project for_the TECHNOCRATS CLUB')

with st.expander('Data'):
   st.write('**Raw data**')
   df=pd.read_csv('https://raw.githubusercontent.com/dataprofessor/palmer-penguins/refs/heads/master/data/penguins_cleaned.csv')
   df
   st.write('**X**')
   X_raw=df.drop('species',axis=1)
   X_raw

   st.write('**y**')
   y_raw=df.species
   y_raw

with st.expander('Data Visualization'):
   st.scatter_chart(data=df,x='bill_length_mm',y='body_mass_g',color='species')
   
#Input Features
with st.sidebar:
   st.header('Input features')
   island=st.selectbox('Island',('Biscoe','Dream','Torgersen'))
   bill_length_mm=st.slider('Bill length(mm)',32.1,59.6,43.9)
   bill_depth_mm=st.slider('Bill Depth(mm)',13.1,21.5,17.2)
   flipper_length_mm=st.slider('Flipper Length(mm)',172.0,231.0,201.0)
   body_mass_g=st.slider('Body Mass(gm)',2700.0,6300.0,4207.0)
   gender=st.selectbox('Gender',('Male','Female'))

#create a Dataframe for the input features
data={'island':island,
   'bill_length_mm':bill_length_mm,
   'bill_depth_mm':bill_depth_mm,
   'flipper_length_mm':flipper_length_mm,
   'body_mass_g':body_mass_g,
   'gender':gender}

input_df=pd.DataFrame(data,index=[0])
input_penguins=pd.concat([input_df,X_raw],axis=0)


with st.expander('Input feautures'):
   st.write('**Input Penguins**')
   input_df
   st.write('**combined penguins data**')
   input_penguins
   
#Data Preparations
#ENCODE X
encode=['Island','gender']
df_penguins=pd.get_dummies(input_penguins,prefix=encode)

X=df_penguins[1:]
input_row=df_penguins[:1]

#Encode y
target_mapper={
   'Adelie':0,
   'Chinstrap':1,
   'Gentoo':2
}
def target_encode(val):
   return target_mapper[val]
   
y=y_raw.apply(target_encode)

#Data Preparations
with st.expander('Data Preparations'):
   st.write('**Encoded X (input penguin)**')
   input_row
   st.write('**Encoded Y (input penguin)**')
   y
   y_raw

#Model Training and inference
#Train the ml model
clf=RandomForestClassifier()
clf.fit(X,y)

##Apply model to make predictions
prediction=clf.predict(input_row)
prediction_proba=clf.predict_proba(input_row)

df_prediction_proba=pd.DataFrame(prediction_proba)
df_prediction_proba.columns=['Adelie','Chinstrap','Gentoo']
df_prediction_proba.rename(columns={0:'Adelie',
                                    1:'Chinstrap',
                                    2:'Gentoo'})
df_prediction_proba

