import numpy as np
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def format(text):
    return [i['name'] for i in ast.literal_eval(text)]

def get_director(text):
    return [i['name'] for i in ast.literal_eval(text) if i['job']=='Director']

def collapse(L):
    return [i.replace(' ','') for i in L]

def recommend(movie):
    index = new[new['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        print(new.iloc[i[0]].title)

credits = pd.read_csv('Movie Datasets/tmdb_5000_credits.csv')
movies = pd.read_csv('Movie Datasets/tmdb_5000_movies.csv')

movies = movies.merge(credits,on='title')

movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.dropna(inplace=True)

movies['genres'] = movies['genres'].apply(format)

movies['keywords'] = movies['keywords'].apply(format)

movies['cast'] = movies['cast'].apply(format)
movies['cast'] = movies['cast'].apply(lambda x:x[0:3])

movies['director'] = movies['crew'].apply(get_director)

movies['cast'] = movies['cast'].apply(collapse)
movies['director'] = movies['director'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)

movies['overview'] = movies['overview'].apply(lambda x:x.split())

movies['attributes'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new = movies.drop(columns=['overview','genres','keywords','cast','crew'])

new['tags'] = new['tags'].apply(lambda x: " ".join(x))


cv = CountVectorizer(max_features=5000,stop_words='english')
vector = cv.fit_transform(new['tags']).toarray()

similarity = cosine_similarity(vector)

recommend