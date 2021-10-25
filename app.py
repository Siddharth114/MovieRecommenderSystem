import streamlit as st
import pandas as pd
import main
from PIL import Image
import requests

st.title('Movie Recommender System')

nav = st.sidebar.radio(label='Navigation', options=['Home', 'Contribute'])

if nav == 'Home':
    st.subheader('Home')
if nav == 'Contribute':
    st.subheader('Contribute')


option = st.selectbox(
     'Choose your movie',
     (i for i in main.titles))
st.write('You selected:', option)
option_img_response = requests.get(f'http://www.omdbapi.com/?t={option}&apikey=f5f824aa')
option_img = option_img_response.json()


st.image(option_img['Poster'], width = 200)

try:
    key = ((main.data.loc[main.data['title'] == option])['keywords']).to_list()
    st.write('This movie has the keywords:', f'{key[0][0]}, {key[0][1]}, {key[0][2]}')
except IndexError:
    pass

rec = main.recommend(option)
images = []
for i in rec:
    pass


st.write('Check out these recommendations:', 
f'{rec[0]}, {rec[1]}, {rec[2]}, {rec[3]}, {rec[4]}')



st.dataframe(main.data)