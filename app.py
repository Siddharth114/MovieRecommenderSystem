import streamlit as st
import pandas as pd

st.title('Movie Recommender System')

nav = st.sidebar.radio('Navigation'['Home', 'Contribute'])

if nav == 'Home':
    st.write('Home')
if nav == 'Contribute':
    st.write('Contribute')

