import streamlit as st
import pandas as pd
import main
from PIL import Image
import requests

st.title('Movie Recommender System')

nav = st.sidebar.radio(label='Navigation', options=['Home', 'Contribute'])

if nav == 'Home':
    st.header('Home')
    option = st.selectbox(
        'Choose your movie',
        (i for i in main.titles))
    st.write('You selected:')
    option_img_response = requests.get(f'http://www.omdbapi.com/?t={option}&apikey=f5f824aa')
    option_img = option_img_response.json()


    st.image(option_img['Poster'], width = 200, caption=option)

    rec = main.recommend(option)
    images = []
    summaries = []
    for i in rec:
        images.append((i,(requests.get(f'http://www.omdbapi.com/?t={i}&apikey=f5f824aa')).json()))
        summaries.append((' '.join(str(v) for v in (((main.data.loc[main.data['title'] == i])['overview']).to_list())[0])))



    st.write('Check out these recommendations:')
    st.image(images[0][1]['Poster'], width=200, caption = f'{images[0][0]}: {summaries[0]}')
    st.image(images[1][1]['Poster'], width=200, caption = f'{images[1][0]}: {summaries[1]}')
    st.image(images[2][1]['Poster'], width=200, caption = f'{images[2][0]}: {summaries[2]}')
    st.image(images[3][1]['Poster'], width=200, caption = f'{images[3][0]}: {summaries[3]}')
    st.image(images[4][1]['Poster'], width=200, caption = f'{images[4][0]}: {summaries[4]}')

if nav == 'Contribute':
    st.header('Contribute')
    st.subheader('Are you aware of a movie that you want as a part of this database?')
    st.write('Submit the title of the movie here')
    with st.form("my_form"):
        title = st.text_input('Movie title', '')
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write('Movie to be updated:', title)
            st.wrte('Your contribution is much appreciated!')