import streamlit as st
import pandas as pd
import main
from PIL import Image
import requests


stop=False

st.title('FlickFinder')

st.markdown('''Introducing FlickFinder, your movie matchmaker with a twist! Tired of endlessly scrolling through streaming platforms, 
desperately seeking that perfect movie night gem? Say no more! 
FlickFinder is here to save the day, bringing you personalized movie recommendations like no other.''')


st.markdown('''We're not your ordinary movie recommender; we've mastered the art of cinematic matchmaking. 
Just tell us your favorite flick, and we'll unleash our algorithmic Cupids to curate a handpicked 
selection of movies that capture the same essence, style, or thrills you adore. Get ready to embark on an unforgettable movie adventure 
tailored just for you. Lights, camera, discover! ''')

nav = st.sidebar.radio(label='Navigation', options=['Home', 'Contribute'])

if nav == 'Home':
    option = st.selectbox(
        'Choose your movie here',
        (i for i in main.titles))
    # print(option)
    st.subheader('You selected:')
    option_img_response = requests.get(f'http://www.omdbapi.com/?t={option}&apikey=f5f824aa')
    option_img = option_img_response.json()


    try:
        st.image(option_img['Poster'], width = 200, caption=option)
    except KeyError:
        st.warning('We haven\'t found sufficient information on this movie yet')
        st.image('/Users/siddharth/Code/Python/MovieRecommenderSystem/error_img.jpg', width = 200)
        stop=True
    
    
    if not stop:
        rec = main.recommend(option)
        images = []
        summaries = []
        for i in rec:
            images.append((i,(requests.get(f'http://www.omdbapi.com/?t={i}&apikey=f5f824aa')).json()))
            summaries.append((' '.join(str(v) for v in (((main.data.loc[main.data['title'] == i])['overview']).to_list())[0])))


        st.subheader('Check out these recommendations:')

        col1, col2, col3 = st.columns(3)

        with col1:
            st.image(images[0][1]['Poster'], width=200, caption = f'{images[0][0]}: {summaries[0]}')
        with col2:
            st.image(images[1][1]['Poster'], width=200, caption = f'{images[1][0]}: {summaries[1]}')
        with col3:
            st.image(images[2][1]['Poster'], width=200, caption = f'{images[2][0]}: {summaries[2]}')

        col4, col5, col6 = st.columns(3)
        with col4:
            st.image(images[3][1]['Poster'], width=200, caption = f'{images[3][0]}: {summaries[3]}')
        with col5:
            st.image(images[4][1]['Poster'], width=200, caption = f'{images[4][0]}: {summaries[4]}')
        with col6:
            st.image(images[5][1]['Poster'], width=200, caption = f'{images[5][0]}: {summaries[5]}')

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

        