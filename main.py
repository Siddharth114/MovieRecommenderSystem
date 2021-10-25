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
    index = training_data[training_data['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        print(training_data.iloc[i[0]].title)

credits = pd.read_csv('Movie Datasets/tmdb_5000_credits.csv')
movies = pd.read_csv('Movie Datasets/tmdb_5000_movies.csv')

data = movies.merge(credits,on='title')

data = data[['movie_id','title','overview','genres','keywords','cast','crew']]

data.dropna(inplace=True)

data['genres'] = data['genres'].apply(format)

data['keywords'] = data['keywords'].apply(format)

data['cast'] = data['cast'].apply(format)
data['cast'] = data['cast'].apply(lambda x:x[0:3])

data['director'] = data['crew'].apply(get_director)

data['cast'] = data['cast'].apply(collapse)
data['director'] = data['director'].apply(collapse)
data['genres'] = data['genres'].apply(collapse)
data['keywords'] = data['keywords'].apply(collapse)

data['overview'] = data['overview'].apply(lambda x:x.split())

data['attributes'] = data['overview'] + data['genres'] + data['keywords'] + data['cast'] + data['director']

training_data = data.drop(columns=['overview','genres','keywords','cast','director'])

training_data['attributes'] = training_data['attributes'].apply(lambda x: " ".join(x))


cv = CountVectorizer(max_features=5000,stop_words='english')
vector = cv.fit_transform(training_data['attributes']).toarray()

similarity = cosine_similarity(vector)

recommend('Batman')